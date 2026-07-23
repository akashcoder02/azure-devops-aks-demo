import json

from security.scan_manager import (
    scan_manager
)


class TrivyParser:

    def __init__(self):

        self.report = (
            scan_manager.application_reports()
            / "trivy"
            / "trivy.json"
        )

    def parse(self):

        if not self.report.exists():

            return {

                "status": "Not Scanned",

                "findings": 0,

                "critical": 0,

                "high": 0,

                "medium": 0,

                "data": []

            }

        try:

            with open(self.report) as file:

                report = json.load(file)

            critical = 0
            high = 0
            medium = 0

            for result in report.get("Results", []):

                for vuln in result.get("Vulnerabilities", []):

                    severity = vuln.get("Severity", "")

                    if severity == "CRITICAL":
                        critical += 1

                    elif severity == "HIGH":
                        high += 1

                    elif severity == "MEDIUM":
                        medium += 1

            return {

                "status": "Completed",

                "findings": critical + high + medium,

                "critical": critical,

                "high": high,

                "medium": medium,

                "data": report

            }

        except Exception:

            return {

                "status": "Error",

                "findings": 0,

                "critical": 0,

                "high": 0,

                "medium": 0,

                "data": []

            }


trivy_parser = TrivyParser()