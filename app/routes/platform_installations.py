from flask import Blueprint, render_template
from flask import jsonify

from services.platform_installations import (
    platform_installations_service
)

platform_installations_bp = Blueprint(
    "platform_installations",
    __name__
)

@platform_installations_bp.route("/platform-installations")
def platform_installations():

    installations = platform_installations_service.get_installations()

    return render_template(
        "platform_installations.html",
        installations=installations
    )

@platform_installations_bp.route(
    "/api/install/argocd",
    methods=["POST"]
)
def install_argocd():

    success = platform_installations_service.trigger(
        "install-argocd.yml"
    )

    return jsonify({
        "success": success,
        "message": "ArgoCD installation triggered."
    })


@platform_installations_bp.route(
    "/api/install/monitoring",
    methods=["POST"]
)
def install_monitoring():

    success = platform_installations_service.trigger(
        "install-monitoring.yml"
    )

    return jsonify({
        "success": success,
        "message": "Monitoring installation triggered."
    })


@platform_installations_bp.route(
    "/api/install/logging",
    methods=["POST"]
)
def install_logging():

    success = platform_installations_service.trigger(
        "logging.yml"
    )

    return jsonify({
        "success": success,
        "message": "Logging installation triggered."
    })

@platform_installations_bp.route(
    "/api/uninstall/argocd",
    methods=["POST"]
)
def uninstall_argocd():

    success = platform_installations_service.uninstall(
        "destroy-argocd.yml"
    )

    return jsonify({
        "success": success,
        "message": "ArgoCD uninstall triggered."
    })


@platform_installations_bp.route(
    "/api/uninstall/monitoring",
    methods=["POST"]
)
def uninstall_monitoring():

    success = platform_installations_service.uninstall(
        "destroy-monitoring.yml"
    )

    return jsonify({
        "success": success,
        "message": "Monitoring uninstall triggered."
    })


@platform_installations_bp.route(
    "/api/uninstall/logging",
    methods=["POST"]
)
def uninstall_logging():

    success = platform_installations_service.uninstall(
        "destroy-logging.yml"
    )

    return jsonify({
        "success": success,
        "message": "Logging uninstall triggered."
    })