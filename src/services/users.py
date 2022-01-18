import os
from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session

def find(username):
    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    return user

def login(username, password):
    sql = "SELECT password, id, role FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        return False
    if not check_password_hash(user[0], password):
        return False

    session["id"] = user[1]
    session["username"] = username
    session["role"] = user[2]
    session["csrf"] = os.urandom(16).hex()
    return True


def register(username, full_name, country, password):
    hash_value = generate_password_hash(password)
    user = find(username)
    if user:
        return user

    try:
        sql = "INSERT INTO users (username, password, full_name, country, role) VALUES (:username, :password, :full_name, :country, :role)"
        db.session.execute(
            sql, {"username": username, "password": hash_value, "full_name": full_name, "country": country, "role": "user"})
        db.session.commit()
        
    except:
        return False

    

def profile(username):
    sql = "SELECT U.username, U.full_name, U.country, (SELECT COUNT(*) as amount FROM reports WHERE user_name=:username ORDER BY amount DESC) FROM users U LEFT JOIN reports R ON U.username = R.user_name WHERE U.username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    return user

def get_reports(username):
    try:
        sql = "SELECT R.id, R.title, TO_CHAR(R.date, 'dd / mm / yyyy'), R.status, C.username, C.name FROM reports R LEFT JOIN companies C ON R.company_name = C.username WHERE user_name=:username"
        result = db.session.execute(sql, {"username": username})
        db.session.commit()
        reports = result.fetchall()
        return reports
    except:
        return False
