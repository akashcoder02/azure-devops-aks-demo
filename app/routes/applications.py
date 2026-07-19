from flask import Blueprint, jsonify, render_template
from services.application_job_manager import run
from services.script_runner import run_script
from services.applications import applications_service

applications = Blueprint("applications", __name__)

ALLOWED_ACTIONS = {
    "deploy",
    "status",
    "undeploy"
}

@applications.route("/applications")
def applications_page():

    apps = applications_service.get_applications()

    return render_template(
        "applications.html",
        applications=apps
    )

@applications.route("/api/applications/<app_name>/<action>", methods=["POST"])
def execute(app_name, action):

    if action not in ALLOWED_ACTIONS:

        return jsonify({
            "success": False,
            "message": "Invalid action"
        }), 400

    script = f"applications/{app_name}/{action}.sh"

    started = run(script)

    return jsonify({
        "success": started
    })


@applications.route("/api/applications/<app_name>/status")
def status(app_name):

    output = run_script(f"applications/{app_name}/status.sh --api")

    data = {}

    for line in output.splitlines():

        if "=" in line:

            key, value = line.split("=", 1)

            data[key] = value

    return jsonify(data)