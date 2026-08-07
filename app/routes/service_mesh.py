from flask import Blueprint, jsonify, render_template, request

from services.service_mesh import (
    get_overview,
    get_traffic_management,
    get_security,
    shift_traffic,
    start_canary,
    rollback_traffic,
    get_application_configuration,
    get_resilience,
    apply_resilience as apply_resilience_service,
    reset_resilience as reset_resilience_service,
    apply_security as apply_security_service,
    destroy_security as destroy_security_service
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

@service_mesh_bp.route("/service-mesh/page/security")
def security_page():
    return render_template("service_mesh/security.html")

@service_mesh_bp.route("/service-mesh/page/resilience")
def resilience_page():

    return render_template(
        "service_mesh/resilience.html"
    )



# ==========================================================
# APIs
# ==========================================================

@service_mesh_bp.route("/api/service-mesh/overview")
def service_mesh_overview():
    return jsonify(get_overview())


@service_mesh_bp.route("/api/service-mesh/traffic")
def service_mesh_traffic():
    return jsonify(get_traffic_management())

@service_mesh_bp.route("/api/service-mesh/security")
def service_mesh_security():
    return jsonify(get_security())

@service_mesh_bp.route("/api/service-mesh/resilience")
def service_mesh_resilience():

    return jsonify(
        get_resilience()
    )


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

# ==========================================================
# TRAFFIC SHIFT
# ==========================================================

@service_mesh_bp.route(
    "/api/service-mesh/traffic-shift",
    methods=["POST"]
)
def traffic_shift():

    payload = request.get_json()

    result = shift_traffic(payload)

    return jsonify(result)


# ==========================================================
# CANARY DEPLOYMENT
# ==========================================================

@service_mesh_bp.route(
    "/api/service-mesh/canary",
    methods=["POST"]
)
def canary():

    print("========== CANARY API CALLED ==========")

    payload = request.get_json()

    print(payload)

    result = start_canary(payload)

    print(result)

    return jsonify(result)


# ==========================================================
# ROLLBACK
# ==========================================================

@service_mesh_bp.route(
    "/api/service-mesh/rollback",
    methods=["POST"]
)
def rollback():

    payload = request.get_json()

    result = rollback_traffic(payload)

    return jsonify(result)

# ==========================================================
# APPLICATION CONFIGURATION
# ==========================================================

@service_mesh_bp.route(
    "/api/service-mesh/application/<application>"
)
def application_configuration(application):

    return jsonify(

        get_application_configuration(application)

    )

# ==========================================================
# APPLY SECURITY
# ==========================================================

@service_mesh_bp.route(
    "/api/service-mesh/security/apply",
    methods=["POST"]
)
def apply_security():

    payload = request.get_json()

    result = trigger_workflow(

        workflow_file="service-mesh-security.yml",

        inputs={

            "action": "apply",

            "mtls_mode": payload.get(
                "mtls_mode",
                "STRICT"
            ),

            "authorization_enabled": payload.get(
                "authorization_enabled",
                True
            ),

            "jwt_enabled": payload.get(
                "jwt_enabled",
                False
            ),

            "jwt_issuer": payload.get(
                "jwt_issuer",
                ""
            ),

            "jwt_jwks_uri": payload.get(
                "jwt_jwks_uri",
                ""
            )

        }

    )

    return jsonify(result)


# ==========================================================
# DESTROY SECURITY
# ==========================================================

@service_mesh_bp.route(
    "/api/service-mesh/security/destroy",
    methods=["POST"]
)
def destroy_security():

    result = trigger_workflow(

        workflow_file="service-mesh-security.yml",

        inputs={

            "action": "destroy"

        }

    )

    return jsonify(result)

# ==========================================================
# APPLY RESILIENCE
# ==========================================================

@service_mesh_bp.route(
    "/api/service-mesh/resilience/apply",
    methods=["POST"]
)
def apply_resilience():

    payload = request.get_json()

    print("\n========== PAYLOAD FROM UI ==========")
    print(payload)
    print("=====================================\n")

    print("\n========== SECURITY REQUEST ==========")
    print(payload)
    print("=====================================\n")

    result = apply_resilience_service(payload)

    return jsonify(result)


# ==========================================================
# RESET RESILIENCE
# ==========================================================

@service_mesh_bp.route(
    "/api/service-mesh/resilience/reset",
    methods=["POST"]
)
def reset_resilience():

    result = reset_resilience_service()

    return jsonify(result)









