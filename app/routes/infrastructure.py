from flask import Blueprint
from flask import jsonify
from flask import request
from flask import render_template

from services.terraform import create_vm

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