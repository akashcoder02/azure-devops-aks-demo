from flask import Blueprint, jsonify, request

from services.script_runner import run_script

api = Blueprint("api", __name__)

ALLOWED_SCRIPTS = {
    "doctor": "doctor.sh",
    "start": "start.sh",
    "stop": "stop.sh"
}


@api.route("/api/run", methods=["POST"])
def run():

    data = request.get_json()

    action = data.get("action")

    if action not in ALLOWED_SCRIPTS:
        return jsonify({
            "success": False,
            "output": "Invalid Action"
        }), 400

    output = run_script(ALLOWED_SCRIPTS[action])

    return jsonify({
        "success": True,
        "output": output
    })