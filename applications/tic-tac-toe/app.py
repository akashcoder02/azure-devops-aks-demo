from flask import Flask, render_template
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(
    __name__,
    static_url_path="/tic-tac-toe/static"
)

app.wsgi_app = ProxyFix(app.wsgi_app)

app.wsgi_app = ProxyFix(app.wsgi_app)
app.config["APPLICATION_ROOT"] = "/tic-tac-toe"


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)