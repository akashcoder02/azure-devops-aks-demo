from pathlib import Path


class ScanManager:

    def __init__(self):

        self.project_root = Path(__file__).resolve().parents[2]

        self.reports = (
            self.project_root /
            "reports" /
            "security"
        )

    def application_reports(self):

        return self.reports / "application"

    def platform_reports(self):

        return self.reports / "platform"

    def history_reports(self):

        return self.reports / "history"


scan_manager = ScanManager()