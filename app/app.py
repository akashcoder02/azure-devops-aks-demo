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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)