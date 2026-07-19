from flask import Blueprint, jsonify

from services.github_status import github_status_service

github_status_bp = Blueprint(
    "github_status",
    __name__
)


@github_status_bp.route("/api/github/status")
def workflow_status():

    return jsonify(
        github_status_service.get_status()
    )