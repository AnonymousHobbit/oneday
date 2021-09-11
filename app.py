
from os import getenv
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

#Basic
@app.route("/")
def index():
    return render_template("index.html")


#Register
@app.route("/register")
def register():
    return render_template("register.html")
    
if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1')
