import json

from security.scan_manager import (
    scan_manager
)


class KubernetesParser:

    def __init__(self):

        self.report = (
            scan_manager.application_reports()
            / "kubernetes"
            / "kubernetes.json"
        )

    def parse(self):

        if not self.report.exists():

            return {

                "status": "Not Run",

                "findings": 0,

                "critical": 0,

                "high": 0,

                "medium": 0,

                "low": 0,

                "data": []

            }

        try:

            with open(self.report, "r") as file:

                data = json.load(file)

            return {

                "status": "Completed",

                "findings": len(data),

                "critical": 0,

                "high": 0,
                "medium": 0,
                "low": len(data),

                "data": data

            }

        except Exception:

            return {

                "status": "Error",

                "findings": 0,

                "critical": 0,

                "high": 0,

                "medium": 0,

                "low": 0,

                "data": []

            }


kubernetes_parser = KubernetesParser()