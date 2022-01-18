from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from os import getenv

load_dotenv()  # access .env file

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
try:
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv(
        "DATABASE_URL")
except:
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv(
        "DATABASE_URL").replace("://", "ql://", 1)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

import routes