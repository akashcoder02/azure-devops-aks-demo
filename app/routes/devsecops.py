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


@devsecops_bp.route("/devsecops/application/gitleaks")
def gitleaks_report():

    data = (
        devsecops_service
        .get_application_security()
    )

    return render_template(
        "gitleaks_report.html",
        data=data["gitleaks"]
    )


@devsecops_bp.route("/devsecops/application/semgrep")
def semgrep_report():

    data = (
        devsecops_service
        .get_application_security()
    )

    return render_template(
        "semgrep_report.html",
        data=data["semgrep"]
    )


@devsecops_bp.route("/devsecops/application/trivy")
def trivy_report():

    data = (
        devsecops_service
        .get_application_security()
    )

    return render_template(
        "trivy_report.html",
        data=data["trivy"]
    )

@devsecops_bp.route("/devsecops/application/pip-audit")
def pip_audit_report():

    data = (
        devsecops_service
        .get_application_security()
    )

    return render_template(
        "pip_audit_report.html",
        data=data["pip-audit"]
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


@devsecops_bp.route("/devsecops/release-gate")
def release_gate_status():

    return release_gate.evaluate()

@devsecops_bp.route("/devsecops/platform/checkov")
def checkov_report():

    data = (
        devsecops_service
        .get_platform_security()
    )

    return render_template(
        "checkov_report.html",
        data=data["checkov"]
    )


@devsecops_bp.route("/devsecops/platform/aks")
def aks_report():

    data = (
        devsecops_service
        .get_platform_security()
    )

    return render_template(
        "aks_report.html",
        data=data["aks"]
    )


@devsecops_bp.route("/devsecops/platform/helm")
def helm_report():

    data = (
        devsecops_service
        .get_platform_security()
    )

    return render_template(
        "helm_report.html",
        data=data["helm"]
    )


@devsecops_bp.route("/devsecops/platform/workflows")
def workflow_report():

    data = (
        devsecops_service
        .get_platform_security()
    )

    return render_template(
        "workflow_report.html",
        data=data["workflows"]
    )


@devsecops_bp.route("/devsecops/platform/dockerfiles")
def dockerfile_report():

    data = (
        devsecops_service
        .get_platform_security()
    )

    return render_template(
        "dockerfile_report.html",
        data=data["dockerfiles"]
    )

@devsecops_bp.route("/devsecops/application/kubernetes")
def kubernetes_report():

    data = (
        devsecops_service
        .get_application_security()
    )

    return render_template(
        "kubernetes_report.html",
        data=data["kubernetes"]
    )

@devsecops_bp.route("/devsecops/analytics")
def security_analytics():

    dashboard = (
        devsecops_service
        .get_dashboard()
    )

    return render_template(
        "security_analytics.html",
        dashboard=dashboard
    )

@devsecops_bp.route("/devsecops/notifications")
def security_notifications():

    dashboard = (
        devsecops_service
        .get_dashboard()
    )

    return render_template(
        "security_notifications.html",
        dashboard=dashboard
    )

@devsecops_bp.route("/devsecops/trends")
def security_trends():

    history = history_manager.read()

    return render_template(
        "security_trends.html",
        history=history
    )