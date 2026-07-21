from flask import (
    Blueprint,
    jsonify,
    render_template
)

from services.platform_actions import (
    platform_actions_service
)

resources_bp = Blueprint(
    "resources",
    __name__
)


@resources_bp.route("/resources")
def resources():
    """
    Azure Resource Center
    """
    return render_template("resources.html")


@resources_bp.route(
    "/api/resources/run",
    methods=["POST"]
)
def run_resources():

    return jsonify(

        platform_actions_service.trigger(
            "azure-running-resources.yml"
        )

    )


@resources_bp.route(
    "/api/resources/status",
    methods=["GET"]
)
def workflow_status():

    return jsonify({

        "status": "running"

    })


@resources_bp.route(
    "/api/resources/report",
    methods=["GET"]
)
def report():

    return jsonify({

        "message": "Report API coming soon."

    })