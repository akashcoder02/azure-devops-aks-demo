from services.security_reports import (
    security_reports_service
)


class ApplicationSecurityService:

    def get_dashboard(self):

        findings = (
            security_reports_service
            .get_gitleaks_report()
        )

        return {

            "summary": {

                "status": (
                    "Completed"
                    if findings
                    else "Not Scanned"
                ),

                "findings": len(findings),

                "critical": len(findings)

            },

            "findings": findings

        }


application_security_service = ApplicationSecurityService()