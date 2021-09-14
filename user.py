import os
from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask import request, session


def login(username, password):
    sql = "SELECT password, id, role FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        return False
    if not check_password_hash(user[0], password):
        return False
    session["user_id"] = user[1]
    session["username"] = username
    session["user_role"] = user[2]
    session["csrf_token"] = os.urandom(16).hex()
    return True

def register(username, password, role):
    hash_value = generate_password_hash(password)

    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()

    if user:
        return user

    try:
        sql = "INSERT INTO users (username, password, role) VALUES (:username, :password, :role)"
        db.session.execute(sql, {"username": username, "password": hash_value, "role":role})
        db.session.commit()
    except:
        return False

    return login(username, password)

def profile(id):
    sql = "SELECT username, role FROM users WHERE id=:user_id"
    result = db.session.execute(sql, {"user_id": id})
    user = result.fetchone()
    print(user)
    return user
