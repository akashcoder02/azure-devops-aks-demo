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