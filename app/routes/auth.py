import os

from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username", "")
        password = request.form.get("password", "")

        expected_username = os.getenv("PORTAL_USERNAME", "admin")
        password_hash = os.getenv("PORTAL_PASSWORD_HASH", "")

        if username == expected_username and password_hash:
            if check_password_hash(password_hash, password):
                session["authenticated"] = True
                session["username"] = username

                next_page = request.args.get("next")

                if next_page:
                    return redirect(next_page)

                return redirect(url_for("dashboard.home"))

        return render_template(
            "login.html",
            error="Invalid username or password"
        )

    return render_template("login.html")


@auth.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("auth.login"))
