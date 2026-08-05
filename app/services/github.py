import requests

from config.github import (
    GITHUB_OWNER,
    GITHUB_REPOSITORY,
    GITHUB_PAT
)


# ==========================================================
# TRIGGER WORKFLOW
# ==========================================================

def trigger_workflow(workflow_file, inputs=None, ref="main"):

    if inputs is None:
        inputs = {}

    url = (
        f"https://api.github.com/repos/"
        f"{GITHUB_OWNER}/{GITHUB_REPOSITORY}"
        f"/actions/workflows/{workflow_file}/dispatches"
    )

    headers = {
        "Authorization": f"Bearer {GITHUB_PAT}",
        "Accept": "application/vnd.github+json"
    }

    payload = {
        "ref": ref,
        "inputs": inputs
    }

    try:

        print("========== GITHUB WORKFLOW ==========")
        print("URL:", url)
        print("Payload:", payload)

        response = requests.post(
            url=url,
            headers=headers,
            json=payload,
            timeout=30
        )

        print("Status Code:", response.status_code)
        print("Response:", response.text)

        if response.status_code == 204:

            return {
                "success": True,
                "message": "Workflow started successfully."
            }

        return {
            "success": False,
            "message": response.text
        }

    except Exception as ex:

        return {
            "success": False,
            "message": str(ex)
        }