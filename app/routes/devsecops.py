from flask import (
    Blueprint,
    render_template
)

from services.devsecops import (
    devsecops_service
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