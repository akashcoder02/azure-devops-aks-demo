from flask import Blueprint, jsonify, request

from services.github_actions import github_actions_service

github_actions_bp = Blueprint(
    "github_actions",
    __name__
)


@github_actions_bp.route(
    "/api/github/release",
    methods=["POST"]
)
def release():

    data = request.get_json()

    result = github_actions_service.release_application(data)

    return jsonify(result)

def trigger_undeploy_application(
    application_name
):

    url = (
        f"{GITHUB_API}"
        "/actions/workflows/"
        "undeploy-application.yml"
        "/dispatches"
    )

    payload = {

        "ref": "main",

        "inputs": {

            "application_name": application_name

        }

    }

    response = requests.post(

        url,

        headers=headers,

        json=payload

    )

    if response.status_code == 204:

        return {

            "success": True,

            "message": (
                "Undeploy workflow started."
            )

        }

    return {

        "success": False,

        "message": (
            "Unable to trigger workflow."
        )

    }