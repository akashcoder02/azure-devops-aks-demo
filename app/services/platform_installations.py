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

            subprocess.run(
                [
                    "kubectl",
                    "get",
                    "namespace",
                    namespace
                ],
                check=True,
                capture_output=True,
                text=True
            )

            return True

        except subprocess.CalledProcessError:

            return False

    def get_installations(self):

        return {

            "argocd": {

                "installed":
                    self.check_namespace("argocd"),

                "namespace":
                    "argocd",

                "version":
                    "v3.1.0"

            },

            "monitoring": {

                "installed":
                    self.check_namespace("monitoring"),

                "namespace":
                    "monitoring",

                "version":
                    "kube-prometheus-stack"

            },

            "logging": {

                "installed":
                    self.check_namespace("logging"),

                "namespace":
                    "logging",

                "version":
                    "Fluent Bit + Loki"

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