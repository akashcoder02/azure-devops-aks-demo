from flask import Blueprint, render_template

resources_bp = Blueprint(
    "resources",
    __name__
)


@resources_bp.route("/resources")
def resources():
    """
    Azure Resource Center
    """
    return render_template("resources.html")