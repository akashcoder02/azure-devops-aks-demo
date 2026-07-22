"""Read-only data collection for the Internal Developer Platform dashboard."""

from __future__ import annotations

import csv
import json
import subprocess
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PLATFORM_CONFIG = PROJECT_ROOT / "platform" / "config" / "platform.env"
DEPLOYMENT_HISTORY = PROJECT_ROOT / "history" / "deployment-history.csv"
HISTORY_FIELDS = [
    "Timestamp",
    "Application",
    "Operation",
    "Image",
    "PreviousImage",
    "Replicas",
    "GitCommit",
    "Workflow",
    "GitHubUser",
    "Status",
    "Remarks",
]


class PlatformDashboardService:
    """Collect and cache non-mutating Azure and Kubernetes status data."""

    cache_seconds = 10

    def __init__(self) -> None:
        self._cache: dict[str, Any] | None = None
        self._cache_created_at = 0.0
        self._lock = threading.Lock()
        self._config = self._load_platform_config()

    def overview(self) -> dict[str, Any]:
        """Return a cached snapshot without changing platform state."""
        with self._lock:
            if self._cache and time.monotonic() - self._cache_created_at < self.cache_seconds:
                return self._cache

            self._cache = self._collect_overview()
            self._cache_created_at = time.monotonic()
            return self._cache

    def _collect_overview(self) -> dict[str, Any]:
        print("Collect overview started")
        nodes = self._kubernetes_nodes()
        pods = self._kubernetes_pods()
        applications = [
            self._application_status("tic-tac-toe"),
            self._application_status("tetris"),
        ]
        infrastructure = self._infrastructure_status()
        observability = self._observability_status()

        return {
            "refreshed_at": datetime.now(timezone.utc).isoformat(),
            "platform_health": self._platform_health(
                infrastructure, nodes, applications, observability
            ),
            "infrastructure": infrastructure,
            "kubernetes": {"nodes": nodes, "pods": pods},
            "applications": applications,
            "gitops": [self._argocd_status(app["name"]) for app in applications],
            "observability": observability,
            "autoscaling": {
                "active_hpas": sum(
                    app["hpa"]["status"] == "Active" for app in applications
                ),
                "applications": len(applications),
            },
            "deployment_history": self._deployment_history(),
        }

    def _infrastructure_status(self) -> dict[str, Any]:
        resource_group = self._config.get("RESOURCE_GROUP", "")
        aks_name = self._config.get("AKS_NAME", self._config.get("AKS_CLUSTER", ""))
        acr_name = self._config.get("ACR_NAME", "")
        keyvault_name = self._config.get("KEYVAULT_NAME", "")
        azure_ready, _ = self._run("az", "account", "show", "--output", "none")
        aks = {}
        if resource_group and aks_name:
            aks = self._json_command(
                "az",
                "aks",
                "show",
                "--resource-group",
                resource_group,
                "--name",
                aks_name,
                "--query",
                "{state:powerState.code,version:kubernetesVersion}",
                "--output",
                "json",
            )

        return {
            "azure": self._state(azure_ready, "Connected", "Not connected"),
            "resource_group": self._resource_state(
                "az", "group", "show", "--name", resource_group
            ),
            "aks": {
                "status": self._state(bool(aks), aks.get("state", "Ready"), "Unavailable"),
                "version": aks.get("version", "—"),
                "name": aks_name or "—",
            },
            "acr": self._resource_state("az", "acr", "show", "--name", acr_name),
            "key_vault": self._resource_state(
                "az", "keyvault", "show", "--name", keyvault_name
            ),
        }

    def _kubernetes_nodes(self) -> dict[str, Any]:
        items = self._json_command("kubectl", "get", "nodes", "--output", "json").get(
            "items", []
        )
        ready = sum(
            any(
                condition.get("type") == "Ready" and condition.get("status") == "True"
                for condition in item.get("status", {}).get("conditions", [])
            )
            for item in items
        )
        return {
            "status": self._state(bool(items), "Ready", "Unavailable"),
            "total": len(items),
            "ready": ready,
        }

    def _kubernetes_pods(self) -> dict[str, Any]:
        items = self._json_command(
            "kubectl", "get", "pods", "--all-namespaces", "--output", "json"
        ).get("items", [])
        running = sum(item.get("status", {}).get("phase") == "Running" for item in items)
        return {"total": len(items), "running": running}

    def _application_status(self, name: str) -> dict[str, Any]:
        deployment = self._json_command(
            "kubectl", "get", "deployment", name, "--output", "json"
        )
        pods = self._json_command(
            "kubectl", "get", "pods", "--selector", f"app={name}", "--output", "json"
        ).get("items", [])
        hpa = self._json_command("kubectl", "get", "hpa", name, "--output", "json")
        ingress = self._json_command(
            "kubectl", "get", "ingress", f"{name}-ingress", "--output", "json"
        )
        deployment_status = deployment.get("status", {})
        containers = deployment.get("spec", {}).get("template", {}).get("spec", {}).get(
            "containers", []
        )
        image = containers[0].get("image", "—") if containers else "—"
        ready = deployment_status.get("readyReplicas", 0) or 0
        desired = deployment.get("spec", {}).get("replicas", 0) or 0
        running = sum(pod.get("status", {}).get("phase") == "Running" for pod in pods)
        ingress_ready = ingress.get("status", {}).get("loadBalancer", {}).get("ingress", [])

        return {
            "name": name,
            "health": self._state(ready > 0, "Healthy", "Unavailable"),
            "pods": {"running": running, "total": len(pods)},
            "replicas": {"ready": ready, "desired": desired},
            "image": image,
            "hpa": self._hpa_status(hpa),
            "ingress": self._state(bool(ingress_ready), "Available", "Not available"),
        }

    def _hpa_status(self, hpa: dict[str, Any]) -> dict[str, Any]:
        if not hpa:
            return {
                "status": "Not configured",
                "current_replicas": 0,
                "min_replicas": 0,
                "max_replicas": 0,
                "cpu": "—",
            }

        spec = hpa.get("spec", {})
        status = hpa.get("status", {})
        cpu = "—"
        for metric in status.get("currentMetrics", []):
            resource = metric.get("resource", {})
            if resource.get("name") == "cpu":
                value = resource.get("current", {}).get("averageUtilization")
                cpu = f"{value}%" if value is not None else "—"
                break

        return {
            "status": "Active",
            "current_replicas": status.get("currentReplicas", 0) or 0,
            "min_replicas": spec.get("minReplicas", 0) or 0,
            "max_replicas": spec.get("maxReplicas", 0) or 0,
            "cpu": cpu,
        }

    def _argocd_status(self, name: str) -> dict[str, Any]:
        application = self._json_command(
            "kubectl",
            "get",
            "application.argoproj.io",
            name,
            "--namespace",
            "argocd",
            "--output",
            "json",
        )
        status = application.get("status", {})
        return {
            "name": name,
            "health": status.get("health", {}).get("status", "Unavailable"),
            "sync": status.get("sync", {}).get("status", "Unavailable"),
            "last_sync": status.get("operationState", {}).get("finishedAt", "—"),
            "auto_sync": bool(
                application.get("spec", {}).get("syncPolicy", {}).get("automated")
            ),
        }

    def _observability_status(self) -> dict[str, dict[str, str]]:
        return {
            "prometheus": self._workload_state(
                "statefulset", "prometheus-kube-prometheus-stack-prometheus", "monitoring"
            ),
            "grafana": self._workload_state(
                "deployment", "kube-prometheus-stack-grafana", "monitoring"
            ),
            "fluent_bit": self._workload_state("daemonset", "fluent-bit", "logging"),
            "loki": self._workload_state("statefulset", "loki", "logging"),
        }

    def _workload_state(self, kind: str, name: str, namespace: str) -> dict[str, str]:
        workload = self._json_command(
            "kubectl", "get", kind, name, "--namespace", namespace, "--output", "json"
        )
        status = workload.get("status", {})
        ready = status.get("readyReplicas", status.get("numberReady", 0)) or 0
        return {"status": self._state(ready > 0, "Healthy", "Unavailable")}

    @staticmethod
    def _platform_health(
        infrastructure: dict[str, Any],
        nodes: dict[str, Any],
        applications: list[dict[str, Any]],
        observability: dict[str, dict[str, str]],
    ) -> dict[str, str]:
        checks = [
            infrastructure["azure"],
            infrastructure["aks"]["status"],
            nodes["status"],
            *(app["health"] for app in applications),
            *(component["status"] for component in observability.values()),
        ]
        healthy = sum(value in {"Connected", "Ready", "Healthy"} for value in checks)
        return {
            "status": "Healthy" if healthy == len(checks) else "Degraded",
            "summary": f"{healthy} of {len(checks)} platform checks are healthy",
        }

    @staticmethod
    def _load_platform_config() -> dict[str, str]:
        if not PLATFORM_CONFIG.exists():
            return {}

        config: dict[str, str] = {}
        for line in PLATFORM_CONFIG.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                config[key.strip()] = value.strip().strip('"').strip("'")
        return config

    @staticmethod
    def _deployment_history() -> list[dict[str, str]]:
        if not DEPLOYMENT_HISTORY.exists():
            return []

        with DEPLOYMENT_HISTORY.open(newline="", encoding="utf-8-sig") as history_file:
            rows = list(csv.reader(history_file))
        return [dict(zip(HISTORY_FIELDS, row)) for row in rows[1:][-10:]][::-1]

    def _resource_state(self, *command: str) -> dict[str, str]:
        if not command[-1]:
            return {"status": "Unavailable"}
        available, _ = self._run(*command, "--output", "none")
        return {"status": self._state(available, "Available", "Unavailable")}

    def _json_command(self, *command: str) -> dict[str, Any]:
        available, output = self._run(*command)
        if not available:
            return {}
        try:
            return json.loads(output)
        except json.JSONDecodeError:
            return {}

    @staticmethod
    def _run(*command: str) -> tuple[bool, str]:
        try:
            result = subprocess.run(
                command,
                cwd=PROJECT_ROOT,
                check=False,
                capture_output=True,
                text=True,
                timeout=4,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False, ""
        return result.returncode == 0, result.stdout.strip()

    @staticmethod
    def _state(available: bool, available_label: str, unavailable_label: str) -> str:
        return available_label if available else unavailable_label
