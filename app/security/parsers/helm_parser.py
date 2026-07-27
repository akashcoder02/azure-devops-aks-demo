import json

from security.scan_manager import (
    scan_manager
)


class HelmParser:

    def __init__(self):

        self.report = (
            scan_manager.platform_reports()
            / "helm"
            / "helm.json"
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

            findings = data.get(
                "findings",
                []
            )

            return {

                "status": "Completed",

                "findings": len(findings),

                "critical": 0,

                "high": len(findings),

                "medium": 0,

                "low": 0,

                "data": findings

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


helm_parser = HelmParser()