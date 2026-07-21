import subprocess


class ApplicationsService:

    def get_public_ip(self):

        try:

            result = subprocess.run(

                [
                    "kubectl",
                    "get",
                    "svc",
                    "ingress-nginx-controller",
                    "-n",
                    "ingress-nginx",
                    "-o",
                    "jsonpath={.status.loadBalancer.ingress[0].ip}"
                ],

                capture_output=True,
                text=True,
                check=True

            )

            return result.stdout.strip()

        except Exception:

            return ""

    def get_applications(self):

        public_ip = self.get_public_ip()

        return [

            {
                "name": "tic-tac-toe",
                "icon": "🎮",
                "status": "Running",
                "namespace": "default",
                "deployment": "GitOps",
                "pods": "2/2",
                "hpa": "Enabled",

                "local_url":
                    "http://localhost:8080/tic-tac-toe",

                "public_url":
                    (
                        f"http://{public_ip}/tic-tac-toe"
                        if public_ip
                        else "#"
                    )

            },

            {
                "name": "tetris",
                "icon": "🧱",
                "status": "Running",
                "namespace": "default",
                "deployment": "Traditional",
                "pods": "1/1",
                "hpa": "Disabled",

                "local_url":
                    "http://localhost:8080/tetris",

                "public_url":
                    (
                        f"http://{public_ip}/tetris"
                        if public_ip
                        else "#"
                    )

            }

        ]


applications_service = ApplicationsService()