import os
from __main__ import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask import request, session

def find(username):
    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    return user

def login(username, password):
    sql = "SELECT password, id, role FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()

    if not user and not check_password_hash(user[0], password):
        return False

    session["id"] = user[1]
    session["username"] = username
    session["role"] = user[2]
    session["csrf"] = os.urandom(16).hex()
    return True


def register(username, full_name, country, password):
    hash_value = generate_password_hash(password)

    if user := find(username):
        return user

    try:
        sql = "INSERT INTO users (username, password, full_name, country, role) VALUES (:username, :password, :full_name, :country, :role)"
        db.session.execute(
            sql, {"username": username, "password": hash_value, "full_name": full_name, "country": country, "role": "user"})
        db.session.commit()
    except:
        return False

    return login(username, password)

def profile(username):
    sql = "SELECT username, full_name, country FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    return user