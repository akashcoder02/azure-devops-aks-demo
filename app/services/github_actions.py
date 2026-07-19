import requests

from config.github import (
    GITHUB_OWNER,
    GITHUB_REPOSITORY,
    GITHUB_PAT,
    RELEASE_WORKFLOW,
    GITHUB_API
)


class GitHubActionsService:

    def release_application(self, data):

        url = (
            f"{GITHUB_API}/repos/"
            f"{GITHUB_OWNER}/"
            f"{GITHUB_REPOSITORY}/"
            f"actions/workflows/"
            f"{RELEASE_WORKFLOW}/dispatches"
        )

        headers = {
            "Authorization": f"Bearer {GITHUB_PAT}",
            "Accept": "application/vnd.github+json"
        }

        payload = {
            "ref": "main",
            "inputs": {
                "application_name": data["application_name"],
                "environment": data["environment"],
                "deployment_strategy": data["deployment_strategy"],
                "deployment_type": data["deployment_type"]
            }
        }

        print("URL:", url)
        print("Payload:", payload)

        response = requests.post(
            url,
            headers=headers,
            json=payload
        )

        if response.status_code == 204:

            return {
                "success": True,
                "message": "Workflow started successfully."
            }

        print("=" * 60)
        print("Status Code:", response.status_code)
        print("Response:", response.text)
        print("=" * 60)

        return {
            "success": False,
            "message": response.text
        }


github_actions_service = GitHubActionsService()