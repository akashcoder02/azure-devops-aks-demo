from flask import Flask, render_template
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.config["APPLICATION_ROOT"] = "/tic-tac-toe"

app.wsgi_app = ProxyFix(app.wsgi_app, x_prefix=1)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)