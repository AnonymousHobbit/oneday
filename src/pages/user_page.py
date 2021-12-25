from flask import Blueprint, render_template, request, redirect, session

#============USERS============
import services.users as users
import services.reports as reports
user_page = Blueprint("user_page", __name__, url_prefix="/users")

#Profile
@user_page.route("/<username>", methods=["GET", "POST"])
def profile(username, error=None):
    if not users.auth():
        return redirect("/login")

    user_data = users.profile(username)
    #user_posts = reports.get_by_user(username)

    if user_data is None:
        return render_template("profile.html", user_data=[username], error=error)
    # user_posts=user_posts
    return render_template("profile.html", user_data=user_data, error=error)

    return redirect("/")

@user_page.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if users.auth():
            return redirect("/")
        return render_template("register/login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not users.login(username.lower(), password):
            return render_template("register/login.html", error="Wrong username or password")

        return redirect("/")


@user_page.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        if users.name() is not None:
            return redirect("/")
        return render_template("register/user.html")

    if request.method == "POST":
        username = request.form["username"]

        if len(username) < 1:
            return render_template("register/user.html", error="Please fill out the username field")

        if len(username) > 17:
            return render_template("register/user.html", error="Username cannot be longer than 17 characters.")

        password = request.form["password"]
        if len(password) == 0:
            return render_template("register/user.html", error="Please fill out the password field")

        full_name = request.form["full_name"] or None

        reg = users.register(username.lower(), password, full_name)

        if not reg:
            return render_template("register/user.html", error="Failed to register")

        return redirect("/")


@user_page.route("/logout")
def logout():
    try:
        del session["username"]
        del session["id"]
        del session["csrf"]
        return redirect("/")
    except:
        return redirect("/login")
