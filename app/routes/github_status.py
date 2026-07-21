from flask import Blueprint, jsonify, request

from services.github_status import github_status_service

from services.deployment_context import deployment_context

github_status_bp = Blueprint(
    "github_status",
    __name__
)


@github_status_bp.route("/api/github/status")
def workflow_status():

    return jsonify(
        github_status_service.get_status()
    )

@github_status_bp.route(
    "/api/github/context",
    methods=["POST"]
)
def save_context():

    data = request.json

    deployment_context["application"] = \
        data["application_name"]

    deployment_context["environment"] = \
        data["environment"]

    deployment_context["strategy"] = \
        data["deployment_strategy"]

    return jsonify({
        "success": True
    })