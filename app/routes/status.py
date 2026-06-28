from flask import Blueprint, jsonify
from services.script_runner import run_script

status = Blueprint("status", __name__)


@status.route("/api/platform-status")
def platform_status():

    output = run_script("status.sh")

    data = {}

    for line in output.splitlines():

        if "=" in line:

            key, value = line.split("=", 1)

            data[key] = value

    return jsonify(data)
