from flask import Blueprint, render_template

from services.argocd import argocd_service

argocd_bp = Blueprint(
    "argocd",
    __name__
)

@argocd_bp.route("/argocd-status")
def argocd_status():

    status = argocd_service.get_status()

    return render_template(
        "argocd_status.html",
        status=status
    )