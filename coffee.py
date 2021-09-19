import os
from app import db
from flask import request, session

def add_new(name):
    try:
        sql = "INSERT INTO coffees (name) VALUES (:name)"
        db.session.execute(sql, {"name": name})
        db.session.commit()
        return True
    except:
        return False

def get_all():
    sql = "SELECT name, id FROM coffees"
    result = db.session.execute(sql)
    coffees = result.fetchall()
    return coffees

