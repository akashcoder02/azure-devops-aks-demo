import json

from security.scan_manager import (
    scan_manager
)


class AKSParser:

    def __init__(self):

        self.report = (
            scan_manager.platform_reports()
            / "aks"
            / "aks.json"
        )

    def parse(self):

        if not self.report.exists():

            return {

                "status": "Not Scanned",

                "cluster": "-",

                "version": "-",

                "data": {}

            }

        try:

            with open(self.report) as file:

                data = json.load(file)

            return {

                "status": "Completed",

                "cluster": data.get("name"),

                "version": data.get(
                    "kubernetesVersion"
                ),

                "data": data

            }

        except Exception:

            return {

                "status": "Error",

                "cluster": "-",

                "version": "-",

                "data": {}

            }


aks_parser = AKSParser()