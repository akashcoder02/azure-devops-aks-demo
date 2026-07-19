from flask import Blueprint
from flask import jsonify
from flask import request
from flask import render_template

from services.terraform import create_vm

from services.kubernetes import (
    get_cluster_status,
    get_node_count,
    get_pod_count,
    get_deployments,
    get_services,
    get_ingress,
    get_hpa
)

infrastructure_bp = Blueprint(
    "infrastructure",
    __name__
)


# Infrastructure Page
@infrastructure_bp.route("/infrastructure")
def infrastructure():

    return render_template("infrastructure.html")


# Provision API
@infrastructure_bp.route("/api/infrastructure/vm", methods=["POST"])
def provision_vm():

    data = request.get_json()

    result = create_vm(
        data["vm_name"],
        data["vm_count"],
        data["vm_template"],
        data["location"],
        data["vm_size"],
        data["admin_username"],
        data["public_key"]
    )

    return jsonify({
        "success": True,
        "message": result, 
        "output": result
})

@infrastructure_bp.route("/api/infrastructure/status")
def infrastructure_status():

    return jsonify({

        "cluster": get_cluster_status(),

        "nodes": get_node_count(),

        "pods": get_pod_count(),

        "deployments": get_deployments(),

        "services": get_services(),

        "ingress": get_ingress(),

        "hpa": get_hpa()

    })