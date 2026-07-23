import json
from pathlib import Path


class DevSecOpsSettingsService:

    def __init__(self):

        self.config = (
            Path(__file__).resolve().parents[1]
            / "config"
            / "devsecops.json"
        )

    def get_settings(self):

        with open(self.config, "r") as file:
            return json.load(file)


devsecops_settings_service = DevSecOpsSettingsService()