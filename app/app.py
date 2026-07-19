from flask import Flask

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

app = Flask(__name__)

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)