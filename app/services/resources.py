import json
import subprocess
from datetime import datetime


class AzureResourceService:
    """Service to collect live Azure and Kubernetes inventory."""

    @staticmethod
    def run_command(command):

        try:

            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=20
            )

            if result.returncode != 0:

                return {
                    "status": "offline",
                    "count": 0,
                    "message": result.stderr.strip(),
                    "items": []
                }

            if result.returncode != 0:

                error = result.stderr.strip()

                if "Unable to connect to the server" in error:
                    message = "AKS Cluster Unavailable"

                elif "Please run 'az login'" in error:
                    message = "Azure Login Required"

                elif "timed out" in error.lower():
                    message = "Command Timed Out"

                else:
                    message = "Command Failed"

                return {
                    "status": "offline",
                    "count": 0,
                    "message": message,
                    "items": []
                }

            output = result.stdout.strip()

            if not output:
                return {
                    "status": "healthy",
                    "count": 0,
                    "message": "OK",
                    "items": []
                }

            data = json.loads(output)

            if isinstance(data, list):
                count = len(data)
            elif isinstance(data, dict) and "items" in data:
                count = len(data["items"])
            else:
                count = 1

            return {
                "status": "healthy",
                "count": count,
                "message": "OK",
                "items": data
            }

        except subprocess.TimeoutExpired:

            return {
                "status": "offline",
                "count": 0,
                "message": "Command Timed Out",
                "items": []
            }

        except Exception:

            return {
                "status": "offline",
                "count": 0,
                "message": "Unexpected Error",
                "items": []
            }

    # -----------------------
    # Azure
    # -----------------------

    @classmethod
    def get_resources(cls):
        return cls.run_command(
            "az resource list --output json"
        )

    @classmethod
    def get_aks(cls):
        return cls.run_command(
            "az aks list --output json"
        )

    @classmethod
    def get_acr(cls):
        return cls.run_command(
            "az acr list --output json"
        )

    @classmethod
    def get_keyvaults(cls):
        return cls.run_command(
            "az keyvault list --output json"
        )

    @classmethod
    def get_public_ips(cls):
        return cls.run_command(
            "az network public-ip list --output json"
        )

    # -----------------------
    # Kubernetes
    # -----------------------

    @classmethod
    def get_nodes(cls):
        return cls.run_command(
            "kubectl get nodes -o json"
        )

    @classmethod
    def get_pods(cls):
        return cls.run_command(
            "kubectl get pods -A -o json"
        )

    @classmethod
    def get_deployments(cls):
        return cls.run_command(
            "kubectl get deployments -A -o json"
        )

    @classmethod
    def get_services(cls):
        return cls.run_command(
            "kubectl get services -A -o json"
        )

    @classmethod
    def get_ingresses(cls):
        return cls.run_command(
            "kubectl get ingress -A -o json"
        )

    @classmethod
    def get_namespaces(cls):
        return cls.run_command(
            "kubectl get namespaces -o json"
        )

    # -----------------------
    # Inventory
    # -----------------------

    @classmethod
    def build_inventory(cls):

        inventory = {

            "azure": {
                "resources": cls.get_resources(),
                "aks": cls.get_aks(),
                "acr": cls.get_acr(),
                "keyvaults": cls.get_keyvaults(),
                "public_ips": cls.get_public_ips()
            },

            "kubernetes": {
                "nodes": cls.get_nodes(),
                "pods": cls.get_pods(),
                "deployments": cls.get_deployments(),
                "services": cls.get_services(),
                "ingresses": cls.get_ingresses(),
                "namespaces": cls.get_namespaces()
            },

            "monitoring": {
                "prometheus": cls.get_prometheus(),
                "grafana": cls.get_grafana()
            },

            "logging": {
                "loki": cls.get_loki(),
                "fluent_bit": cls.get_fluent_bit()
            },

            "gitops": {
                "pods": cls.get_argocd_pods(),
                "applications": cls.get_argocd_applications()
            },

            "applications": {
                "deployments": cls.get_application_deployments(),
                "services": cls.get_application_services(),
                "ingresses": cls.get_application_ingresses()
            },

        }

        sections = [
            inventory["azure"]["resources"],
            inventory["azure"]["aks"],
            inventory["azure"]["acr"],
            inventory["azure"]["keyvaults"],
            inventory["azure"]["public_ips"],
            inventory["kubernetes"]["nodes"],
            inventory["kubernetes"]["pods"],
            inventory["kubernetes"]["deployments"],
            inventory["kubernetes"]["services"],
            inventory["kubernetes"]["ingresses"],
            inventory["kubernetes"]["namespaces"]
        ]

        healthy = sum(
            1 for section in sections
            if section["status"] == "healthy"
        )

        inventory["summary"] = {
            "resources": inventory["azure"]["resources"]["count"],
            "healthy": healthy,
            "offline": len(sections) - healthy,
            "warnings": 0,
            "last_scan": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        inventory["platform"] = {

            "azure_connected":
                inventory["azure"]["resources"]["status"] == "healthy",

            "aks_available":
                inventory["azure"]["aks"]["status"] == "healthy"
                and inventory["azure"]["aks"]["count"] > 0,

            "kubernetes_connected":
                inventory["kubernetes"]["nodes"]["status"] == "healthy"

        }

        return inventory

    # -----------------------
    # Inventory
    # -----------------------

    @classmethod
    def get_prometheus(cls):
        return cls.run_command(
            "kubectl get pods -n monitoring -l app.kubernetes.io/name=prometheus -o json"
        )


    @classmethod
    def get_grafana(cls):
        return cls.run_command(
            "kubectl get pods -n monitoring -l app.kubernetes.io/name=grafana -o json"
        )

    @classmethod
    def get_loki(cls):
        return cls.run_command(
            "kubectl get pods -n logging -l app.kubernetes.io/name=loki -o json"
        )

    @classmethod
    def get_fluent_bit(cls):
        return cls.run_command(
            "kubectl get pods -n logging -l app.kubernetes.io/name=fluent-bit -o json"
        )

    @classmethod
    def get_argocd_pods(cls):
        return cls.run_command(
            "kubectl get pods -n argocd -o json"
        )

    @classmethod
    def get_argocd_applications(cls):
        return cls.run_command(
            "kubectl get applications -n argocd -o json"
        )

    @classmethod
    def get_application_deployments(cls):
        return cls.run_command(
            "kubectl get deployments -A -o json"
        )

    @classmethod
    def get_application_services(cls):
        return cls.run_command(
            "kubectl get svc -A -o json"
        )

    @classmethod
    def get_application_ingresses(cls):
        return cls.run_command(
            "kubectl get ingress -A -o json"
        )