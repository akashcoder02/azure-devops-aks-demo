import json

from security.scan_manager import (
    scan_manager
)


class TrivyParser:

    def parse(self):

        report = (
            scan_manager.application_reports()
            / "trivy.json"
        )

        if not report.exists():

            return {

                "status": "Not Run",

                "findings": 0,

                "critical": 0,

                "high": 0,

                "medium": 0,

                "low": 0,

                "data": []

            }

        with open(report) as file:

            data = json.load(file)

        critical = 0
        high = 0
        medium = 0
        low = 0

        for result in data.get("Results", []):

            for vuln in result.get(
                "Vulnerabilities",
                []
            ):

                severity = vuln.get("Severity")

                if severity == "CRITICAL":
                    critical += 1

                elif severity == "HIGH":
                    high += 1

                elif severity == "MEDIUM":
                    medium += 1

                elif severity == "LOW":
                    low += 1

        total = (

            critical +

            high +

            medium +

            low

        )

        return {

            "status": "Completed",

            "findings": total,

            "critical": critical,

            "high": high,

            "medium": medium,

            "low": low,

            "data": data.get("Results", [])

        }


trivy_parser = TrivyParser()