import json
from pathlib import Path


class BaseParser:

    def __init__(self, report_path: Path):

        self.report = report_path

    def empty_result(self):

        return {
            "status": "Not Scanned",
            "findings": 0,
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "data": []
        }

    def parse(self):

        if not self.report.exists():
            return self.empty_result()

        try:

            with open(self.report, "r") as file:
                data = json.load(file)

            scan_time = None
            findings = data

            if isinstance(data, dict):
                scan_time = data.get("scan_time")
                findings = data.get("findings", [])

            return {
                "status": "Completed",
                "scan_time": scan_time,
                "findings": len(findings),
                "critical": 0,
                "high": 0,
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