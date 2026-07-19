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
                "hpa": "Enabled"
            },

            {
                "name": "tetris",
                "icon": "🧱",
                "status": "Running",
                "namespace": "default",
                "deployment": "Traditional",
                "pods": "1/1",
                "hpa": "Disabled"
            }

        ]


applications_service = ApplicationsService()