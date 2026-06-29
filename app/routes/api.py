from flask import Blueprint, jsonify, request

from services.job_manager import run, job

api = Blueprint("api", __name__)

ALLOWED_SCRIPTS = {

    # Platform
    "doctor": "doctor.sh",
    "start": "start.sh",
    "stop": "stop.sh --auto",
}


@api.route("/api/run", methods=["POST"])
def execute():

    data = request.get_json()

    action = data["action"]

    if action not in ALLOWED_SCRIPTS:

        return jsonify({
            "success": False
        })

    started = run(ALLOWED_SCRIPTS[action])

    return jsonify({
        "success": started
    })


@api.route("/api/status")
def status():

    return jsonify(job)