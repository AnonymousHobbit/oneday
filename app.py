
from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from os import getenv

#Custom modules
import user

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")


load_dotenv()  # access .env file

db_url = getenv("DATABASE_URL")

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

#Default route
@app.route("/")
def index():
    return render_template("index.html")

#Profile


@app.route("/users/<id>", methods=["GET", "POST"])
def profile(id):
    if session and session["user_id"] == int(id):
        user_data = user.profile(id)
        return render_template("profile.html", user_data=user_data)
    return redirect("/")
    


#login
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
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
        return render_template("register.html")
    
    if request.method == "POST":
        username = request.form["username"]

        if len(username) < 1:
            return render_template("register.html", error="Please fill out the username field")

        if len(username) > 17:
            return render_template("register.html", error="Username cannot be longer than 17 characters.")

        password = request.form["password"]
        if len(password) == 0:
            return render_template("register.html", error="Please fill out the password field")
        
        role = request.form["role"]
        if role not in ("1", "2"):
            return render_template("register.html", error="Error setting a role")
        reg = user.register(username.lower(), password, role)

        #Check if username already exists and isnt the same as roles
        if reg not in (True, False):
            return render_template("register.html", error="Username already exists")

        if not reg:
            return render_template("register.html", error="Failed to register")
        print(session)
        return redirect("/")
        

@app.route("/logout")
def logout():
    del session["username"]
    del session["user_role"]
    del session["user_id"]
    return redirect("/")
    
if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1')
