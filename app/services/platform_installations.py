class PlatformInstallationsService:

    def get_installations(self):
        return {
            "argocd": {
                "installed": True,
                "namespace": "argocd",
                "version": "v3.1.0"
            },
            "monitoring": {
                "installed": True,
                "namespace": "monitoring",
                "version": "kube-prometheus-stack"
            },
            "logging": {
                "installed": True,
                "namespace": "logging",
                "version": "Fluent Bit + Loki"
            }
        }


platform_installations_service = PlatformInstallationsService()