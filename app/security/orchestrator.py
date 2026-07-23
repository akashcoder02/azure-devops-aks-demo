from security.scan_manager import (
    scan_manager
)

from security.scanner_registry import (
    get_application_scanners,
    get_platform_scanners
)


class DevSecOpsOrchestrator:
    """
    Central DevSecOps Orchestrator.
    """

    def __init__(self):

        self.scan_manager = scan_manager

    def application_security(self):

        results = {}

        for scanner in get_application_scanners():

            results[
                scanner.name.lower()
            ] = scanner.run()

        results["available_scans"] = [

            "Secrets",
            "SAST",
            "Dependencies",
            "Containers",
            "Kubernetes"

        ]

        return results

    def platform_security(self):

        results = {}

        for scanner in get_platform_scanners():

            results[
                scanner.name.lower()
            ] = scanner.run()

        results["available_scans"] = [

            "Terraform",
            "AKS",
            "Helm",
            "Workflows",
            "Dockerfiles"

        ]

        return results

    def dashboard_summary(self):

        return {

            "application": (
                self.application_security()
            ),

            "platform": (
                self.platform_security()
            )

        }


devsecops_orchestrator = DevSecOpsOrchestrator()