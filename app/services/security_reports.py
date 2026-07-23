from pathlib import Path
import json


class SecurityReportsService:

    def __init__(self):

        self.project_root = Path(__file__).resolve().parents[2]

    def get_gitleaks_report(self):

        report = (
            self.project_root
            / "reports"
            / "security"
            / "application"
            / "secrets"
            / "gitleaks.json"
        )

        if not report.exists():
            return []

        with open(report, "r") as file:
            return json.load(file)


security_reports_service = SecurityReportsService()