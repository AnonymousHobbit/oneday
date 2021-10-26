import os
from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask import request, session

def create(content, id):
    try:
        sql = "INSERT INTO posts (content, author_id) values (:content, :author_id)"
        db.session.execute(sql, {"content": content, "author_id": id})
        db.session.commit()
        return True
    except:
        return False

def get_all():
    try:
       sql = "SELECT P.id, U.name, U.username, P.content FROM users U, posts P WHERE U.id = P.author_id ORDER BY P.id desc"
       result = db.session.execute(sql)
       db.session.commit()
       posts = result.fetchall()
       return posts
    except:
        return False

def get_by_user(username):
    try:
        sql = "SELECT id, content FROM posts WHERE author_id = (SELECT id FROM users WHERE username=:username)"
        result = db.session.execute(sql, {"username": username})
        db.session.commit()
        posts = result.fetchall()
        return posts
    except:
        return False

def get_by_id(username, post_id):
    try:
        sql = "SELECT P.id, U.name, U.username, P.content FROM users U, posts P WHERE P.id=:post_id AND U.username=:username"
        result = db.session.execute(sql, {"post_id": post_id, "username":username})
        db.session.commit()
        post = result.fetchone()
        return post
    except:
        return False