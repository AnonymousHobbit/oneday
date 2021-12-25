from flask import Blueprint, render_template, redirect

import services.users as users
import services.reports as reports

home_page = Blueprint("home_page", __name__)


@home_page.route("/")
def index():
    if not users.auth():
        return redirect("/users/login")
    all_posts = reports.get_all()
    return render_template("index.html", posts=all_posts)

@home_page.route("/register")
def register():
    return render_template("register/index.html")
