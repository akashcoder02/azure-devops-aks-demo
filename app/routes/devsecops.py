from flask import (
    Blueprint,
    render_template
)

from services.devsecops import (
    devsecops_service
)

from security.history_manager import (
    history_manager
)

from services.policy_service import (
    policy_service
)

from services.release_gate import (
    release_gate
)

devsecops_bp = Blueprint(
    "devsecops",
    __name__
)

@devsecops_bp.route("/devsecops")
def devsecops():

    dashboard = (
        devsecops_service
        .get_dashboard()
    )

    return render_template(
        "devsecops.html",
        dashboard=dashboard
    )

@devsecops_bp.route("/devsecops/application")
def application_security():

    data = (
        devsecops_service
        .get_application_security()
    )

    return render_template(
        "application_security.html",
        data=data
    )


@devsecops_bp.route("/devsecops/platform")
def platform_security():

    data = (
        devsecops_service
        .get_platform_security()
    )

    return render_template(
        "platform_security.html",
        platform=data
    )


@devsecops_bp.route("/devsecops/policies")
def security_policies():

    return render_template(
        "security_policies.html"
    )


@devsecops_bp.route("/devsecops/reports")
def security_reports():

    return render_template(

        "security_reports.html",

        application=(
            devsecops_service
            .get_application_security()
        ),

        platform=(
            devsecops_service
            .get_platform_security()
        )

    )


@devsecops_bp.route("/devsecops/history")
def security_history():

    history = history_manager.read()

    return render_template(

        "security_history.html",

        history=history

    )

@devsecops_bp.route("/devsecops/policy-status")
def policy_status():

    return policy_service.evaluate()

@devsecops_bp.route(
    "/devsecops/release-gate"
)
def release_gate_status():

    return release_gate.evaluate()