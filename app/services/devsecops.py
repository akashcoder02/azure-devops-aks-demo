from security.orchestrator import (
    devsecops_orchestrator
)
from security.scoring.security_score import (
    security_score
)

class DevSecOpsService:

    def get_dashboard(self):
        dashboard = (
            devsecops_orchestrator
            .dashboard_summary()
        )

        dashboard["score"] = (
            security_score.calculate(dashboard)
        )

        return dashboard

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