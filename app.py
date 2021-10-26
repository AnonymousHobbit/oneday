from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, session, abort
from dotenv import load_dotenv
from os import getenv

load_dotenv()  # access .env file


app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

## Initialize Database
db_url = getenv("DATABASE_URL")

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

#Custom modules
import user
import posts

#Default route
@app.route("/")
def index():
    if not user.auth():
        return redirect("/login")
    all_posts = posts.get_all()
    return render_template("index.html", posts=all_posts)

#============POSTS============

@app.route("/posts/create", methods=["POST"])
def create_post():
    if not user.auth():
        return redirect("/login")

    if not user.csrf():
            return render_template("error.html", error="CSRF Token missing")

    content = request.form["content"]
    posts.create(content, user.id())
    return redirect("/")

@app.route("/<username>/<post_id>")
def view_post(username, post_id):
    if not user.auth():
        return redirect("/login")
    
    post_data = posts.get_by_id(username, post_id)
    return render_template("post.html", post=post_data)

#============USERS============

#Profile
@app.route("/<username>", methods=["GET", "POST"])
def profile(username, error=None):
    if not user.auth():
        return redirect("/login")

    user_data = user.profile(username)
    user_posts = posts.get_by_user(username)

    if user_data is None:
        return render_template("profile.html", user_data=[username], error=error)
    return render_template("profile.html", user_data=user_data, user_posts=user_posts, error=error)
    
    return redirect("/")
    
#login
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        if user.auth():
            return redirect("/")
        return render_template("login.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not user.login(username.lower(), password):
            return render_template("login.html", error="Wrong username or password")

        return redirect("/")

#Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        if user.name() is not None:
            return redirect("/")
        return render_template("register.html")
    
    if request.method == "POST":
        username = request.form["username"]

        if len(username) < 1:
            return render_template("register.html", error="Please fill out the username field")

        if len(username) > 17:
            return render_template("register.html", error="Username cannot be longer than 17 characters.")

        name = request.form["name"]
        if len(name) < 1:
            return render_template("register.html", error="Name cannot be empty")

        country = request.form["country"]
        if len(name) < 1:
            return render_template("register.html", error="Country cannot be empty")

        password = request.form["password"]
        if len(password) == 0:
            return render_template("register.html", error="Please fill out the password field")
        
        reg = user.register(name, country, username.lower(), password)

        #Check if username already exists and isnt the same as roles
        if reg not in (True, False):
            return render_template("register.html", error="Username already exists")

        if not reg:
            return render_template("register.html", error="Failed to register")

        return redirect("/")
        

@app.route("/logout")
def logout():
    try:
        del session["username"]
        del session["id"]
        del session["csrf"]
        return redirect("/")
    except:
        return redirect("/login")
        

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1')