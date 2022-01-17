import os
from __main__ import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

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
    sql = "SELECT id, username, name, country, email, description FROM companies WHERE username=:username"
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


def get_all():

    sql = "SELECT DISTINCT C.username, C.name, (SELECT ABS(NOW()::date - date::date) FROM reports WHERE C.username = company_name ORDER BY date DESC LIMIT 1) FROM companies C LEFT JOIN reports R ON C.username = R.company_name"
    result = db.session.execute(sql)
    companies = result.fetchall()
    return companies

def update_description(username, description):
    sql = "UPDATE companies SET description=:description WHERE username=:username"
    db.session.execute(sql, {"description": description, "username": username})
    db.session.commit()

def get_reports_list(username):
    sql = "SELECT id, title, status, user_name, TO_CHAR(date, 'dd / mm / yyyy') FROM reports WHERE company_name=:company_name ORDER BY date ASC"
    result = db.session.execute(sql, {"company_name": username})
    reports = result.fetchall()
    return reports