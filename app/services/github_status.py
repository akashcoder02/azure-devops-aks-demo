import requests

from config.github import (
    GITHUB_API,
    GITHUB_OWNER,
    GITHUB_PAT,
    GITHUB_REPOSITORY
)


class GitHubStatusService:

    def get_status(self):

        url = (
            f"{GITHUB_API}/repos/"
            f"{GITHUB_OWNER}/"
            f"{GITHUB_REPOSITORY}/"
            "actions/runs?per_page=1"
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

            return {
                "status": "Unknown",
                "workflow": "-",
                "branch": "-",
                "url": ""
            }

        data = response.json()

        if not data["workflow_runs"]:

            return {
                "status": "No Runs",
                "workflow": "-",
                "branch": "-",
                "url": ""
            }

        run = data["workflow_runs"][0]

        return {
            "status": run["status"],
            "conclusion": run["conclusion"],
            "workflow": run["name"],
            "branch": run["head_branch"],
            "url": run["html_url"],
            "application": "-",
            "environment": "-",
            "strategy": "-",
            "created_at": run["created_at"],
            "updated_at": run["updated_at"],
            "run_number": run["run_number"],
        }


github_status_service = GitHubStatusService()