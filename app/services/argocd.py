import json
import subprocess


class ArgoCDService:

    def get_argocd_version(self):

        try:

            result = subprocess.run(

                [
                    "kubectl",
                    "get",
                    "deployment",
                    "argocd-server",
                    "-n",
                    "argocd",
                    "-o",
                    "jsonpath={.spec.template.spec.containers[0].image}"
                ],

                capture_output=True,
                text=True,
                check=True

            )

            image = result.stdout.strip()

            if ":" in image:

                return image.split(":")[-1]

            return image

        except Exception:

            return "-"

    def get_status(self):

        try:

            result = subprocess.run(

                [
                    "kubectl",
                    "get",
                    "applications",
                    "-n",
                    "argocd",
                    "-o",
                    "json"
                ],

                capture_output=True,
                text=True,
                check=True

            )

            data = json.loads(result.stdout)

            applications = []

            for app in data["items"]:

                applications.append({

                    "name":
                        app["metadata"]["name"],

                    "namespace":
                        app["spec"]["destination"]["namespace"],

                    "sync":
                        app["status"]["sync"]["status"],

                    "health":
                        app["status"]["health"]["status"],

                    "revision":
                        app["status"]["sync"]["revision"][:7]

                })

            return {

                "server": "Running",

                "version":
                    self.get_argocd_version(),

                "applications":
                    applications

            }

        except Exception:

            return {

                "server": "Stopped",

                "version": "-",

                "applications": []

            }


argocd_service = ArgoCDService()