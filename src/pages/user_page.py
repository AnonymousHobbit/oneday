from flask import Blueprint, render_template, request, redirect, session
import requests
#============USERS============
import services.users as users
import services.common as common
import services.reports as reports
user_page = Blueprint("user_page", __name__, url_prefix="/users")

@user_page.route("/<username>/reports/<company_name>/create")
def report_create(username, company_name):
    if request.method == "GET":
        if not common.auth():
            return redirect("/users/login")
        return render_template("reports/create.html")

#Profile
@user_page.route("/<username>", methods=["GET", "POST"])
def profile(username, error=None):
    if not common.auth():
        return redirect("/login")

    user_data = users.profile(username)

    if user_data is None:
        return render_template("user_profile.html", user=[username], error=error)
    # user_posts=user_posts
    return render_template("user_profile.html", user=user_data, error=error)


@user_page.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if common.auth():
            return redirect("/")
        return render_template("login/user.html")

    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        if not users.login(username.lower(), password):
            return render_template("login/user.html", error="Wrong username or password")

        return redirect("/")


@user_page.route("/register", methods=["GET", "POST"])
def register():

    r = requests.get("https://restcountries.com/v3.1/all")
    countries = r.json()

    if request.method == "POST":
        username = request.form["username"].strip()
        full_name = request.form["full_name"] or None
        country = request.form["country"]
        password = request.form["password"]

        #Check if username is long enough
        if len(username) < 1 or len(username) > 20:
            return render_template("register/user.html", error="Username must be between 1 and 20 characters", countries=countries)
        
        #Check if passwor  is not empty
        if len(password) == 0:
            return render_template("register/user.html", error="Please fill out the password field", countries=countries)

        #Check if country exists
        if len(country) == 0:
            return render_template("register/user.html", error="Please select your country", countries=countries)
        
        #Check if registration was successful
        if users.register(username.lower(), full_name, country, password):
            return render_template("register/user.html", error="Username already exists", countries=countries)

        return redirect("/")
    
    if common.username() is not None:
        return redirect("/")

    return render_template("register/user.html", countries=countries)


@user_page.route("/logout")
def logout():
    try:
        del session["username"]
        del session["id"]
        del session["csrf"]
        return redirect("/")
    except:
        return redirect("/login")
