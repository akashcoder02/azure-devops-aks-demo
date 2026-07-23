from security.orchestrator import (
    devsecops_orchestrator
)


class DevSecOpsService:

    def get_dashboard(self):
        return (
            devsecops_orchestrator
            .dashboard_summary()
        )

    def get_application_security(self):
        return (
            devsecops_orchestrator
            .application_security()
        )

    def get_platform_security(self):
        return (
            devsecops_orchestrator
            .platform_security()
        )


devsecops_service = DevSecOpsService()