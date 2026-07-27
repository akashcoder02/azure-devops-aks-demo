import json

from security.scan_manager import (
    scan_manager
)


class CheckovParser:

    def __init__(self):

        self.report = (
            scan_manager.platform_reports()
            / "terraform"
            / "checkov.json"
        )

    def parse(self):

        if not self.report.exists():

            return {

                "status": "Not Scanned",

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

            failed_checks = (
                data.get("results", {})
                    .get("failed_checks", [])
            )

            return {

                "status": "Completed",

                "findings": len(failed_checks),

                "critical": 0,

                "high": len(failed_checks),

                "medium": 0,

                "low": 0,

                "data": failed_checks

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


checkov_parser = CheckovParser()