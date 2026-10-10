from flask import Blueprint, render_template, request, redirect, url_for, session
from models.user import create_user, login_user
auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = login_user(email, password)

        if user:

            session["user_id"] = user["id"]
            session["user_name"] = user["fullname"]
            session["email"] = user["email"]

            return redirect(url_for("chat.chat_page"))

        else:

            return "Invalid Email or Password"

    return render_template("login.html")


@auth.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]

        success = create_user(fullname, email, password)

        if success:

            return redirect(url_for("auth.login"))

        else:

            return "User already exists."

    return render_template("signup.html")

@auth.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("main.home"))