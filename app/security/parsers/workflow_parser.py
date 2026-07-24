import json

from security.scan_manager import (
    scan_manager
)


class WorkflowParser:

    def __init__(self):

        self.report = (
            scan_manager.platform_reports()
            / "workflows"
            / "workflow.json"
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

            findings = data.get(
                "findings",
                []
            )

            return {

                "status": "Completed",

                "findings": len(findings),

                "critical": len(findings),

                "data": findings

            }

        except Exception:

            return {

                "status": "Error",

                "findings": 0,

                "critical": 0,

                "data": []

            }


workflow_parser = WorkflowParser()