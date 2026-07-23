from security.scan_manager import (
    scan_manager
)

from security.scanner_registry import (
    APPLICATION_SCANNERS,
    PLATFORM_SCANNERS
)


class DevSecOpsOrchestrator:
    """
    Central DevSecOps Orchestrator.
    """

    def __init__(self):

        self.scan_manager = scan_manager

    def application_security(self):

        results = {}

        for scanner in APPLICATION_SCANNERS:

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

        for scanner in PLATFORM_SCANNERS:

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
            "application": self.application_security(),
            "platform": self.platform_security()
        }


devsecops_orchestrator = DevSecOpsOrchestrator()