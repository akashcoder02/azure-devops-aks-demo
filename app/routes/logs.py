from flask import Blueprint
from flask import jsonify

from services.logging import (
    get_fluentbit_status,
    get_loki_status
)

logs_bp = Blueprint(
    "logs",
    __name__
)


@logs_bp.route("/api/logging")
def logging_status():

    return jsonify({

        "fluentbit": get_fluentbit_status(),

        "loki": get_loki_status()

    })