import os
from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask import request, session

def login(username, password):
    sql = "SELECT password, id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()

    if not user:
        return False
    if not check_password_hash(user[0], password):
        return False

    session["id"] = user[1]
    session["username"] = username
    session["csrf"] = os.urandom(16).hex()
    return True

def register(name, country, username, password):
    hash_value = generate_password_hash(password)

    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()

    if user:
        return user

    try:
        sql = "INSERT INTO users (name, country, username, password) VALUES (:name, :country, :username, :password)"
        db.session.execute(sql, {"name": name, "country": country, "username": username, "password": hash_value})
        db.session.commit()
    except:
        return False

    return login(username, password)

def profile(username):
    sql = "SELECT name, username, country FROM users WHERE username=:user_name"
    result = db.session.execute(sql, {"user_name": username})
    user = result.fetchone()
    return user

def id():
    return session.get("id", 0)

def csrf():
    if session.get("csrf", 0) == request.form["csrf"]:
        return True
    else:
        return False

def name():
    return session.get("username", None)

def auth():
    if session.get("id", 0) > 0 and session.get("username", None) is not None:
        return True
    return False