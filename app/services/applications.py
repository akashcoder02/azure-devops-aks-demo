class ApplicationsService:

    def get_applications(self):

        return [

            {
                "name": "tic-tac-toe",
                "icon": "🎮",
                "status": "Running",
                "namespace": "default",
                "deployment": "GitOps",
                "pods": "2/2",
                "hpa": "Enabled",
                "url": "http://localhost:8080/tic-tac-toe"
            },

            {
                "name": "tetris",
                "icon": "🧱",
                "status": "Running",
                "namespace": "default",
                "deployment": "Traditional",
                "pods": "1/1",
                "hpa": "Disabled",
                "url": "http://localhost:8080/tetris"
            }

        ]


applications_service = ApplicationsService()