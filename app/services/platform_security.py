class PlatformSecurityService:

    def get_dashboard(self):

        return {
            "terraform": "Not Implemented",
            "aks": "Not Implemented",
            "helm": "Not Implemented",
            "workflows": "Not Implemented",
            "dockerfiles": "Not Implemented"
        }


platform_security_service = PlatformSecurityService()