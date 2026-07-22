import json

from services.script_runner import run_script


class HPAService:

    def get_hpas(self):

        output = run_script(
            "kubectl get hpa -o json"
        )

        try:

            data = json.loads(output)

        except Exception:

            return []

        hpas = []

        for item in data.get("items", []):

            cpu_target = "-"

            current_cpu = "-"

            for metric in item["spec"].get("metrics", []):

                if (
                    metric.get("resource", {})
                    .get("name")
                    == "cpu"
                ):

                    cpu_target = (
                        metric["resource"]
                        ["target"]
                        .get(
                            "averageUtilization",
                            "-"
                        )
                    )

            for metric in item.get(
                "status",
                {}
            ).get(
                "currentMetrics",
                []
            ):

                if (
                    metric.get("resource", {})
                    .get("name")
                    == "cpu"
                ):

                    current_cpu = (
                        metric["resource"]
                        ["current"]
                        .get(
                            "averageUtilization",
                            "-"
                        )
                    )

            hpas.append({

                "name":
                    item["metadata"]["name"],

                "namespace":
                    item["metadata"]["namespace"],

                "min_replicas":
                    item["spec"].get(
                        "minReplicas",
                        1
                    ),

                "max_replicas":
                    item["spec"]["maxReplicas"],

                "current_replicas":
                    item["status"].get(
                        "currentReplicas",
                        0
                    ),

                "desired_replicas":
                    item["status"].get(
                        "desiredReplicas",
                        0
                    ),

                "cpu_target":
                    cpu_target,

                "current_cpu":
                    current_cpu

            })

        return hpas


hpa_service = HPAService()