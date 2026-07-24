import json

from security.scan_manager import (
    scan_manager
)


class AKSParser:

    def __init__(self):

        self.report = (
            scan_manager.platform_reports()
            / "aks"
            / "aks.json"
        )

    def parse(self):

        if not self.report.exists():

            return {

                "status": "Not Scanned",

                "cluster": "-",

                "version": "-",

                "rbac": "Unknown",

                "network_policy": "Unknown",

                "azure_policy": "Unknown",

                "private_cluster": "Unknown",

                "pod_security": "Unknown"

            }

        try:

            with open(self.report, "r") as file:

                data = json.load(file)

            return {

                "status": data.get(
                    "status",
                    "Completed"
                ),

                "cluster": data.get(
                    "cluster",
                    "-"
                ),

                "version": data.get(
                    "version",
                    "-"
                ),

                "rbac": data.get(
                    "rbac",
                    "Unknown"
                ),

                "network_policy": data.get(
                    "network_policy",
                    "Unknown"
                ),

                "azure_policy": data.get(
                    "azure_policy",
                    "Unknown"
                ),

                "private_cluster": data.get(
                    "private_cluster",
                    "Unknown"
                ),

                "pod_security": data.get(
                    "pod_security",
                    "Unknown"
                )

            }

        except Exception:

            return {

                "status": "Error",

                "cluster": "-",

                "version": "-",

                "rbac": "Unknown",

                "network_policy": "Unknown",

                "azure_policy": "Unknown",

                "private_cluster": "Unknown",

                "pod_security": "Unknown"

            }


aks_parser = AKSParser()