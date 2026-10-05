from dotenv import load_dotenv

load_dotenv()
from flask import Flask, request, redirect, url_for, session
import os
from routes.auth import auth

from routes.dashboard import dashboard
from routes.api import api
from routes.status import status
from routes.applications import applications
from routes.infrastructure import infrastructure_bp
from routes.monitoring import monitoring_bp
from routes.logs import logs_bp
from routes.platform_installations import platform_installations_bp
from routes.argocd import argocd_bp
from routes.github_actions import github_actions_bp
from routes.github_status import github_status_bp
from routes.deployment_history import deployment_history_bp
from routes.platform_actions import platform_actions_bp
from routes.resources import resources_bp
from routes.hpa import hpa_bp
from routes.devsecops import (
    devsecops_bp
)
from routes.application_security import (
    application_security_bp
)
from routes.service_mesh import service_mesh_bp

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")


app.register_blueprint(dashboard)
app.register_blueprint(api)
app.register_blueprint(status)
app.register_blueprint(applications)
app.register_blueprint(platform_installations_bp)
app.register_blueprint(argocd_bp)
app.register_blueprint(infrastructure_bp)
app.register_blueprint(monitoring_bp)
app.register_blueprint(logs_bp)
app.register_blueprint(github_actions_bp)
app.register_blueprint(github_status_bp)
app.register_blueprint(deployment_history_bp)
app.register_blueprint(platform_actions_bp)
app.register_blueprint(resources_bp)
app.register_blueprint(hpa_bp)
app.register_blueprint(
    devsecops_bp
)
app.register_blueprint(
    application_security_bp
)
app.register_blueprint(service_mesh_bp)
app.register_blueprint(auth)

@app.before_request
def require_login():

    allowed_endpoints = {
        "auth.login",
        "auth.logout",
    }

    if request.endpoint in allowed_endpoints:
        return

    if request.endpoint == "static":
        return

    if request.path == "/health":
        return

    if not session.get("authenticated"):
        return redirect(
            url_for("auth.login", next=request.path)
        )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)