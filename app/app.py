from flask import Flask

from routes.dashboard import dashboard
from routes.api import api
from routes.status import status

app = Flask(__name__)

app.register_blueprint(dashboard)
app.register_blueprint(api)
app.register_blueprint(status)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)