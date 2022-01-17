from flask import Blueprint, render_template, request, redirect, session, abort
import requests
#============USERS============
import services.users as users
import services.common as common
import services.reports as reports
import services.companies as companies
user_page = Blueprint("user_page", __name__, url_prefix="/users")
    

@user_page.route("/<username>/reports/<report_id>", methods=["GET"])
def report(username, report_id):
    if not common.auth():
        return redirect("/login")

    user_data = [common.username(), common.role()]
    report_data = reports.get_full(report_id)
    messages = reports.get_messages(report_id)

    if username != report_data[10]:
        return abort(403)

    common.permissions(report_data[10], report_data[9])

    if report_data is None:
        return abort(404)
    return render_template("reports/view.html", data=report_data, user=user_data, messages=messages)


@user_page.route("/<username>/reports/<report_id>/edit", methods=["POST"])
def report_close(username, report_id):
    if not common.auth():
        return redirect("/login")
    status = request.form["status"]
    report_data = reports.get_full(report_id)

    if username != report_data[10]:
        return abort(403)

    if status not in ["open", "closed", "accepted"]:
        return redirect(f"/users/{username}/reports/{report_id}")

    common.permissions(report_data[9])
    common.csrf_check()

    reports.close(report_id, status)
    return redirect(f"/users/{username}/reports/{report_id}")

@user_page.route("/<username>/reports/<report_id>/message", methods=["POST"])
def report_message(username, report_id):
    if not common.auth():
        return redirect("/login")
    common.csrf_check()
    message = request.form["message"]
    if len(message) < 3:
        return redirect(f"/users/{username}/reports/{report_id}")
    report_data = reports.get_full(report_id)

    if username != report_data[10]:
        return abort(403)

    common.permissions(report_data[10], report_data[9])

    if not reports.add_message(report_id, message):
        return abort(500)
    return redirect(f"/users/{username}/reports/{report_id}")

@user_page.route("/<username>/reports/<company_name>/create", methods=["GET", "POST"])
def report_create(username, company_name):
    scope = companies.get_scope(company_name)
    data = [username, company_name]
    if request.method == "GET":
        if not common.auth():
            return redirect("/users/login")
        
        return render_template("reports/create.html", data=data, scope=scope)
    
    if request.method == "POST":
        
        if not common.auth():
            return redirect("/users/login")
        common.permissions(username)
        common.csrf_check()

        title = request.form["title"]
        domain = request.form["domain"]
        endpoint = request.form["endpoint"] or None
        description = request.form["description"]
        severity = request.form["severity"]
        status = "open"
        if len(title) < 3 or len(domain) < 3 or len(description) < 3 or len(severity) < 1:
            return redirect(f"/users/{username}/reports/{company_name}/create")
        
        if not reports.create(title, domain, endpoint, description, severity, status, data):
            return render_template("reports/create.html", data=data, error="Something went wrong")
        
        return redirect(f"/users/{username}")

#Profile
@user_page.route("/<username>", methods=["GET"], strict_slashes=False)
def profile(username, error=None):
    if not common.auth():
        return redirect("/login")

    user_data = users.profile(username)
    user_reports = users.get_reports(username)
    common.permissions(username)
    if user_data is None:
        return abort(404)
    
    return render_template("user_profile.html", user=user_data, reports=user_reports, error=error)


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
        del session["role"]
        return redirect("/")
    except:
        return redirect("/login")
