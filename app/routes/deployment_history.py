from flask import Blueprint, jsonify

from services.deployment_history import (
    deployment_history_service
)

deployment_history_bp = Blueprint(
    "deployment_history",
    __name__
)


@deployment_history_bp.route(
    "/api/deployments"
)
def deployments():

    return jsonify(
        deployment_history_service.get_history()
    )