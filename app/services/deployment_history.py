import requests

from config.github import (
    GITHUB_API,
    GITHUB_OWNER,
    GITHUB_REPOSITORY,
    GITHUB_PAT,
    RELEASE_WORKFLOW
)


class DeploymentHistoryService:

    def get_history(self):

        url = (
            f"{GITHUB_API}/repos/"
            f"{GITHUB_OWNER}/"
            f"{GITHUB_REPOSITORY}/"
            f"actions/workflows/"
            f"{RELEASE_WORKFLOW}/runs?per_page=10"
        )

        headers = {
            "Authorization": f"Bearer {GITHUB_PAT}",
            "Accept": "application/vnd.github+json"
        }

        response = requests.get(
            url,
            headers=headers
        )

        if response.status_code != 200:

            return []

        runs = response.json()["workflow_runs"]

        history = []

        for run in runs:

            history.append({

                "id": run["id"],

                "name": run["name"],

                "status": run["status"],

                "conclusion": run["conclusion"],

                "branch": run["head_branch"],

                "created_at": run["created_at"],

                "updated_at": run["updated_at"],

                "url": run["html_url"]

            })

        return history


deployment_history_service = DeploymentHistoryService()