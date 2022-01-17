import os
from __main__ import db
from flask import request, session
from werkzeug.security import check_password_hash, generate_password_hash

import services.reports as reports
import services.users as users

def find(username):
    sql = "SELECT id FROM companies WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    company = result.fetchone()
    return company


def login(username, password):
    sql = "SELECT password, id, role FROM companies WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    company = result.fetchone()

    if not company and not check_password_hash(company[0], password):
        return False

    session["id"] = company[1]
    session["username"] = username
    session["role"] = company[2]
    session["csrf"] = os.urandom(16).hex()
    return True


def register(name, username, email, country, password):
    hash_value = generate_password_hash(password)

    if company := find(username):
        return company

    try:
        sql = "INSERT INTO companies (name, username, email, country, password, role) VALUES (:name, :username, :email, :country, :password, :role)"
        db.session.execute(
            sql, {"name": name, "username": username, "email": email, "country": country, "password": hash_value, "role": "company"})
        db.session.commit()
        
    except:
        return False


def profile(username):
    sql = "SELECT id, username, name, country FROM companies WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    return user

def is_authenticated(username):
   
    if username == session.get("username", None):
        return True
    return False

def add_scope(url):
    sql = "INSERT INTO scope (url, company_id) VALUES (:url, :company_id)"
    db.session.execute(sql, {"url": url, "company_id": session["id"]})
    db.session.commit()

def get_scope(username):
    sql = "SELECT id, url FROM scope WHERE company_id=(select id from companies where username=:username)"
    result = db.session.execute(sql, {"username": username})
    scope = result.fetchall()
    return scope

def delete_scope(id):
    sql = "DELETE FROM scope WHERE id=:id"
    db.session.execute(sql, {"id": id})
    db.session.commit()