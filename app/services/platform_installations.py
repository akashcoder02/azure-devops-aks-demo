import json
import os
import requests
import subprocess

from config.github import (
    GITHUB_API,
    GITHUB_OWNER,
    GITHUB_REPOSITORY,
    GITHUB_PAT
)


class PlatformInstallationsService:


    def check_namespace(self, namespace):

        try:

            result = subprocess.run(
                ["kubectl", "get", "namespace", namespace],
                capture_output=True,
                text=True
            )

            print("Return code:", result.returncode)
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)

            return result.returncode == 0

        except Exception as e:

            print(e)
            return False

    def get_namespaces(self):

        try:

            result = subprocess.run(

                [
                    "kubectl",
                    "get",
                    "namespaces",
                    "-o",
                    "json"
                ],

                capture_output=True,
                text=True,
                check=True

            )

            data = json.loads(result.stdout)

            namespaces = {

                item["metadata"]["name"]

                for item in data["items"]

            }

            return namespaces

        except Exception as e:

            print(e)

            return set()

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
            print("ArgoCD Image:", image)

            if ":" in image:

                return image.split(":")[-1]

            return image

        except Exception:

            return "-"

    def get_argocd_applications(self):

        try:

            result = subprocess.run(

                [
                    "kubectl",
                    "get",
                    "applications",
                    "-n",
                    "argocd",
                    "--no-headers"
                ],

                capture_output=True,
                text=True,
                check=True

            )

            return len(result.stdout.strip().splitlines())

        except Exception:

            return 0

    def get_monitoring_version(self):

        try:

            result = subprocess.run(

                [
                    "kubectl",
                    "get",
                    "deployment",
                    "kube-prometheus-stack-grafana",
                    "-n",
                    "monitoring",
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

    def get_logging_version(self):

        try:

            result = subprocess.run(

                [
                    "kubectl",
                    "get",
                    "daemonset",
                    "fluent-bit",
                    "-n",
                    "logging",
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

    def get_installations(self):

        namespaces = self.get_namespaces()

        return {

            "argocd": {

                "installed":
                    "argocd" in namespaces,

                "namespace":
                    "argocd",

                "version":
                    self.get_argocd_version(),

                "applications":
                    self.get_argocd_applications()

            },

            "monitoring": {

                "installed":
                     "monitoring" in namespaces,

                "namespace":
                    "monitoring",

                "version":
                    self.get_monitoring_version()

            },

            "logging": {

                "installed":
                    "logging" in namespaces,

                "namespace":
                    "logging",

                "version":
                    self.get_logging_version()

            }

        }

    def trigger(self, workflow):

        url = (
            f"{GITHUB_API}/repos/"
            f"{GITHUB_OWNER}/"
            f"{GITHUB_REPOSITORY}/"
            f"actions/workflows/"
            f"{workflow}/dispatches"
        )

        headers = {
            "Authorization": f"Bearer {GITHUB_PAT}",
            "Accept": "application/vnd.github+json"
        }

        payload = {
            "ref": "main"
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload
        )

        print("=" * 60)
        print("URL:", url)
        print("Workflow:", workflow)
        print("Status:", response.status_code)
        print("Response:", response.text)
        print("=" * 60)

        return response.status_code == 204

    def uninstall(self, workflow):

        return self.trigger(workflow)


platform_installations_service = PlatformInstallationsService()