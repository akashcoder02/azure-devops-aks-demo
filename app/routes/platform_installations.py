from flask import Blueprint, render_template

from services.platform_installations import (
    platform_installations_service
)

platform_installations_bp = Blueprint(
    "platform_installations",
    __name__
)

@platform_installations_bp.route("/platform-installations")
def platform_installations():

    installations = platform_installations_service.get_installations()

    return render_template(
        "platform_installations.html",
        installations=installations
    )