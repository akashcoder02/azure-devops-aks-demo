from flask import Blueprint
from flask import jsonify
from flask import render_template

from services.platform_dashboard import PlatformDashboardService

dashboard = Blueprint("dashboard", __name__)

dashboard_service = PlatformDashboardService()


@dashboard.route("/")
def home():

    return render_template("dashboard.html")


@dashboard.route("/health")
def health():

    return jsonify({

        "status": "OK"

    })


@dashboard.route("/api/dashboard")
def dashboard_data():

    return jsonify(

        dashboard_service.overview()

    )