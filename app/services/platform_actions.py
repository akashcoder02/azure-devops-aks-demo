import requests

from config.github import (
    GITHUB_API,
    GITHUB_OWNER,
    GITHUB_REPOSITORY,
    GITHUB_PAT
)


class PlatformActionsService:

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
            "ref": "main",
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload
        )

        return response.status_code == 204


platform_actions_service = PlatformActionsService()