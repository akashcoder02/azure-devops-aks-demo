import json

from datetime import datetime

from security.scan_manager import (
    scan_manager
)


class HistoryManager:

    def __init__(self):

        self.history = (
            scan_manager.history_reports()
            / "history.json"
        )

    def read(self):

        if not self.history.exists():

            return []

        try:

            with open(self.history, "r") as file:

                return json.load(file)

        except Exception:

            return []

    def add(

        self,

        scanner,

        category,

        status,

        findings,

        critical

    ):

        history = self.read()

        history.append(

            {

                "scanner": scanner,

                "category": category,

                "status": status,

                "findings": findings,

                "critical": critical,

                "timestamp": (
                    datetime.now()
                    .strftime("%Y-%m-%d %H:%M:%S")
                )

            }

        )

        with open(self.history, "w") as file:

            json.dump(

                history,

                file,

                indent=4

            )


history_manager = HistoryManager()