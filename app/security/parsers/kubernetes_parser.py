import json

from security.scan_manager import (
    scan_manager
)


class KubernetesParser:

    def __init__(self):

        self.report = (
            scan_manager.application_reports()
            / "kubernetes"
            / "kubernetes.json"
        )


    def parse(self):

        if not self.report.exists():

            return {

                "status": "Not Run",

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


            findings = []


            for item in data:

                object_name = item.get(
                    "object",
                    "-"
                )


                parts = object_name.split("/")


                kind = (
                    parts[0]
                    if len(parts) > 0
                    else "-"
                )


                resource = (
                    parts[1]
                    if len(parts) > 1
                    else "-"
                )


                resource_parts = resource.split(".")


                name = (
                    resource_parts[0]
                    if len(resource_parts) > 0
                    else "-"
                )


                namespace = (
                    resource_parts[1]
                    if len(resource_parts) > 1
                    else "-"
                )


                advises = (
                    item
                    .get("scoring", {})
                    .get("advise", [])
                )


                if advises:

                    for advise in advises:

                        findings.append({

                            "kind": kind,

                            "name": name,

                            "namespace": namespace,

                            "issue": advise.get(
                                "reason",
                                "-"
                            ),

                            "severity": "LOW"

                        })


                else:

                    findings.append({

                        "kind": kind,

                        "name": name,

                        "namespace": namespace,

                        "issue": item.get(
                            "message",
                            "-"
                        ),

                        "severity": "LOW"

                    })


            return {

                "status": "Completed",

                "findings": len(findings),

                "critical": 0,

                "high": 0,

                "medium": 0,

                "low": len(findings),

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


kubernetes_parser = KubernetesParser()