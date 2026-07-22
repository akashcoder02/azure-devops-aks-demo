from flask import Blueprint, jsonify, render_template

from services.hpa import hpa_service


hpa_bp = Blueprint(
    "hpa",
    __name__
)


@hpa_bp.route("/hpa")
def hpa_page():

    hpas = hpa_service.get_hpas()

    return render_template(
        "hpa.html",
        hpas=hpas
    )


@hpa_bp.route("/api/hpa")
def hpa_api():

    return jsonify(
        hpa_service.get_hpas()
    )