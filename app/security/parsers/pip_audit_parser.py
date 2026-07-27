import json

from security.scan_manager import (
    scan_manager
)


class PipAuditParser:

    def __init__(self):

        self.report = (
            scan_manager.application_reports()
            / "dependencies"
            / "pip-audit.json"
        )


    def parse(self):

        if not self.report.exists():

            return {

                "status": "Not Run",

                "findings": 0,

                "critical": 0,

                "data": []

            }


        try:

            with open(self.report, "r") as file:

                data = json.load(file)


            vulnerabilities = []


            for dependency in data.get(
                "dependencies",
                []
            ):

                for vulnerability in dependency.get(
                    "vulns",
                    []
                ):

                    vulnerabilities.append(
                        vulnerability
                    )


            return {

                "status": "Completed",

                "findings": len(vulnerabilities),

                "critical": len(vulnerabilities),

                "data": vulnerabilities

            }


        except Exception:


            return {

                "status": "Error",

                "findings": 0,

                "critical": 0,

                "data": []

            }


pip_audit_parser = PipAuditParser()