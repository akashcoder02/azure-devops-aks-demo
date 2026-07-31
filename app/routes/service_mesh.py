from flask import Blueprint, jsonify, render_template

from services.service_mesh import (
    get_overview,
    get_traffic_management
)

from services.github import trigger_workflow


service_mesh_bp = Blueprint(
    "service_mesh",
    __name__
)


# ==========================================================
# DASHBOARD
# ==========================================================

@service_mesh_bp.route("/service-mesh")
def service_mesh():
    return render_template("service_mesh.html")


# ==========================================================
# PAGES
# ==========================================================

@service_mesh_bp.route("/service-mesh/page/overview")
def overview_page():
    return render_template("service_mesh/overview.html")


@service_mesh_bp.route("/service-mesh/page/traffic")
def traffic_page():
    return render_template("service_mesh/traffic_management.html")


# ==========================================================
# APIs
# ==========================================================

@service_mesh_bp.route("/api/service-mesh/overview")
def service_mesh_overview():
    return jsonify(get_overview())


@service_mesh_bp.route("/api/service-mesh/traffic")
def service_mesh_traffic():
    return jsonify(get_traffic_management())


@service_mesh_bp.route("/api/service-mesh/refresh")
def refresh():
    return jsonify(get_overview())


@service_mesh_bp.route("/api/service-mesh/status")
def status():
    return jsonify(get_overview())


# ==========================================================
# INSTALL
# ==========================================================

@service_mesh_bp.route("/api/service-mesh/install", methods=["POST"])
def install():

    result = trigger_workflow(
        workflow_file="install-service-mesh.yml"
    )

    return jsonify(result)


# ==========================================================
# DESTROY
# ==========================================================

@service_mesh_bp.route("/api/service-mesh/destroy", methods=["POST"])
def destroy():

    result = trigger_workflow(
        workflow_file="destroy-service-mesh.yml"
    )

    return jsonify(result)