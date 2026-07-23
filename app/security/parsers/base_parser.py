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
            "data": []
        }

    def parse(self):

        if not self.report.exists():
            return self.empty_result()

        try:

            with open(self.report, "r") as file:
                data = json.load(file)

            return {
                "status": "Completed",
                "findings": len(data),
                "critical": len(data),
                "data": data
            }

        except Exception:

            return {
                "status": "Error",
                "findings": 0,
                "critical": 0,
                "data": []
            }