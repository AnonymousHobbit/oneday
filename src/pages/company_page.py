from flask import Blueprint, render_template, request, redirect, session, abort
import requests

import services.users as users
import services.reports as reports
import services.companies as companies
import services.common as common

company_page = Blueprint("company_page", __name__, url_prefix="/companies")



#Profile
@company_page.route("/<company_name>/edit/scope/add", methods=["POST"])
def scope_add(company_name):
    if not common.auth():
        return redirect("/login")

    url = request.form["url"]
    companies.add_scope(url)

    return redirect(f"/companies/{company_name}")


@company_page.route("/", methods=["GET"], strict_slashes=False)
def index_page():
    if not common.auth():
        return redirect("/login")
    company = companies.get_all()
    print(company)
    return render_template("companies.html", companies=company)

@company_page.route("/<company_name>/edit/scope/delete", methods=["POST"])
def scope_delete(company_name):
    if not common.auth():
        return redirect("/login")

    common.csrf_check()
    url = request.form["url_id"]
    companies.delete_scope(url)

    return redirect(f"/companies/{company_name}")


@company_page.route("/<username>", methods=["GET", "POST"], strict_slashes=False)
def profile(username, error=None):
    if not common.auth():
        return redirect("/login")

    permissions = None
    if common.role() == "company" and companies.is_authenticated(username):
        permissions = True

    user_data = [common.username(), common.role(), permissions]
    company_data = companies.profile(username)
    scope = companies.get_scope(username)
    if company_data is None:
        return abort(404)
    return render_template("company_profile.html", company=company_data, user=user_data, scope=scope, error=error)


@company_page.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if common.username() is not None:
            return redirect("/")

        return render_template("login/company.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not companies.login(username.lower(), password):
            return render_template("login/company.html", error="Wrong username or password")

        return redirect("/")

@company_page.route("/register", methods=["GET", "POST"])
def register():
    r = requests.get("https://restcountries.com/v3.1/all")
    countries = r.json()
        
    if request.method == "POST":
        
        name = request.form["name"]
        username = request.form["username"]
        email = request.form["email"]
        country = request.form["country"]
        password = request.form["password"]
        

        #Check if username is not empty
        if len(name) < 1 and len(username) < 1:
            return render_template("register/company.html", error="Please fill out the name field", countries=countries)
        
        #Check if password is not empty
        if len(password) == 0:
            return render_template("register/company.html", error="Please fill out the password field", countries=countries)
        
        #Check if country exists
        if len(country) == 0:
            return render_template("register/company.html", error="Please select your country", countries=countries)
        
        #Check if registration was successful
        if companies.register(name, username, email, country, password):
            return render_template("register/company.html", error="Company already exists", countries=countries)

        if common.username() is not None:
            return redirect("/")

    return render_template("register/company.html", countries=countries)



@company_page.route("/logout")
def logout():
    try:
        del session["id"]
        del session["username"]
        del session["role"]
        del session["csrf"]
        return redirect("/")
    except:
        return redirect("/login")
        

