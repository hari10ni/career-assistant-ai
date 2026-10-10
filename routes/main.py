from flask import Blueprint, render_template, session, redirect, url_for

from models.chat import get_dashboard_stats

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("index.html")


@main.route("/about")
def about():
    return render_template("about.html")


@main.route("/contact")
def contact():
    return render_template("contact.html")


@main.route("/dashboard")
def dashboard():

    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )

    stats = get_dashboard_stats(
        session["user_id"]
    )

    return render_template(
        "dashboard.html",
        stats=stats
    )