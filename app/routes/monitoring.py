from flask import Blueprint
from flask import jsonify

from services.monitoring import (
    get_prometheus_status,
    get_grafana_status
)

monitoring_bp = Blueprint(
    "monitoring",
    __name__
)


@monitoring_bp.route("/api/monitoring")
def monitoring_status():

    return jsonify({

        "prometheus": get_prometheus_status(),

        "grafana": get_grafana_status()

    })