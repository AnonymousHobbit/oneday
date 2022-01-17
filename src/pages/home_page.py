from flask import Blueprint, render_template, redirect, session

import services.users as users
import services.reports as reports
import services.common as common

home_page = Blueprint("home_page", __name__)


@home_page.route("/")
def index():
    role = common.role()
    username = common.username()

    if common.auth():
        if role == "company":
            return redirect(f"/companies/{username}")
        
        if role == "user":
            return redirect(f"/users/{username}")
    return render_template("index.html", role=role, username=username)

@home_page.route("/register")
def register():
    return render_template("register/index.html")

@home_page.route("/login")
def login():
    return render_template("login/index.html")
