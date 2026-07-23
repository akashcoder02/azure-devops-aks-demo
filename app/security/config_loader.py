import json
from pathlib import Path


class ConfigLoader:

    def __init__(self):

        self.config = (
            Path(__file__).resolve().parents[1]
            / "config"
            / "devsecops.json"
        )

    def load(self):

        with open(self.config, "r") as file:
            return json.load(file)


config_loader = ConfigLoader()