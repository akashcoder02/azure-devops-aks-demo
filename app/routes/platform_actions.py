from flask import Blueprint, jsonify

from services.platform_actions import (
    platform_actions_service
)

platform_actions_bp = Blueprint(
    "platform_actions",
    __name__
)


@platform_actions_bp.route(
    "/api/platform/start",
    methods=["POST"]
)
def start_platform():

    success = platform_actions_service.trigger(
        "infra.yaml"
    )

    return jsonify({
        "success": success,
        "message": (
            "Platform Start Triggered"
            if success
            else
            "Unable to trigger platform."
        )
    })


@platform_actions_bp.route(
    "/api/platform/stop",
    methods=["POST"]
)
def stop_platform():

    success = platform_actions_service.trigger(
        "destroy.yaml"
    )

    return jsonify({
        "success": success,
        "message": (
            "Platform Destroy Triggered"
            if success
            else
            "Unable to trigger destroy."
        )
    })