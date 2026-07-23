from flask import Blueprint, render_template

platform_security_bp = Blueprint(
    "platform_security",
    __name__
)


@platform_security_bp.route("/devsecops/platform")
def platform_security():

    return render_template(
        "platform_security.html"
    )