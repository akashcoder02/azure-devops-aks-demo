import json
import subprocess


class HPAService:

    def get_hpas(self):

        try:

            output = subprocess.check_output(
                [
                    "kubectl",
                    "get",
                    "hpa",
                    "-o",
                    "json"
                ],
                text=True
            )

            data = json.loads(output)

        except Exception as ex:

            print(f"HPA Error: {ex}")

            return []

        hpas = []

        for item in data.get("items", []):

            cpu_target = "-"

            current_cpu = "-"

            spec_metrics = (
                item.get("spec", {}).get("metrics") or []
            )

            for metric in spec_metrics:

                if metric.get("resource", {}).get("name") == "cpu":

                    cpu_target = metric["resource"]["target"].get(
                        "averageUtilization",
                        "-"
                    )

            current_metrics = (
                item.get("status", {}).get("currentMetrics") or []
            )

            for metric in current_metrics:

                if metric.get("resource", {}).get("name") == "cpu":

                    current_cpu = metric["resource"]["current"].get(
                        "averageUtilization",
                        "-"
                    )

            hpas.append({

                "name": item["metadata"]["name"],

                "namespace": item["metadata"]["namespace"],

                "current_replicas": item["status"].get(
                    "currentReplicas",
                    0
                ),

                "desired_replicas": item["status"].get(
                    "desiredReplicas",
                    0
                ),

                "min_replicas": item["spec"].get(
                    "minReplicas",
                    1
                ),

                "max_replicas": item["spec"]["maxReplicas"],

                "cpu_target": cpu_target,

                "current_cpu": current_cpu

            })

        return hpas


hpa_service = HPAService()