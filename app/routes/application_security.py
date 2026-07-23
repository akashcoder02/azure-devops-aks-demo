from flask import (
    Blueprint,
    render_template
)

from services.application_security import (
    application_security_service
)


application_security_bp = Blueprint(
    "application_security",
    __name__
)


@application_security_bp.route(
    "/devsecops/application"
)
def application_security():

    data = (
        application_security_service
        .get_dashboard()
    )

    return render_template(
        "application_security.html",
        data=data
    )