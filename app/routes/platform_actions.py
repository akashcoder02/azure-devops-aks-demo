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

@platform_actions_bp.route( 
    "/api/platform/doctor",
    methods=["POST"]
)
def doctor():

    success = platform_actions_service.trigger( 
        "platform-doctor.yaml"
    )

    return jsonify({
        "success": success,
        "message": "Platform Doctor Triggered"
    })


@platform_actions_bp.route(
    "/api/platform/status",
    methods=["POST"]
)
def status():

    success = platform_actions_service.trigger(
        "platform-status.yaml"
    )

    return jsonify({
        "success": success,
        "message": "Platform Status Triggered"
    })


@platform_actions_bp.route(
    "/api/platform/resources",
    methods=["POST"]
)
def resources():

    success = platform_actions_service.trigger(
        "azure-running-resources.yml"
    )

    return jsonify({
        "success": success,
        "message": "Running Resources Triggered"
    })