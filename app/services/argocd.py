class ArgoCDService:

    def get_status(self):
        return {
            "server": "Running",
            "version": "v3.1.0",
            "applications": [
                {
                    "name": "tic-tac-toe",
                    "namespace": "default",
                    "sync": "Synced",
                    "health": "Healthy",
                    "revision": "a34fd11"
                },
                {
                    "name": "tetris",
                    "namespace": "default",
                    "sync": "Synced",
                    "health": "Healthy",
                    "revision": "b921ac2"
                }
            ]
        }


argocd_service = ArgoCDService()