from __main__ import db

def create(content, id):
    try:
        sql = "INSERT INTO reports (content, author_id) values (:content, :author_id)"
        db.session.execute(sql, {"content": content, "author_id": id})
        db.session.commit()
        return True
    except:
        return False

def get_all():
    try:
       sql = "SELECT P.id, U.name, U.username, P.content FROM users U, reports P WHERE U.id = P.author_id ORDER BY P.id desc"
       result = db.session.execute(sql)
       db.session.commit()
       reports = result.fetchall()
       return reports
    except:
        return False

def get_by_user(username):
    try:
        sql = "SELECT id, content FROM reports WHERE author_id = (SELECT id FROM users WHERE username=:username)"
        result = db.session.execute(sql, {"username": username})
        db.session.commit()
        reports = result.fetchall()
        return reports
    except:
        return False

def get_by_id(username, post_id):
    try:
        sql = "SELECT P.id, U.name, U.username, P.content FROM users U, reports P WHERE P.id=:post_id AND U.username=:username"
        result = db.session.execute(sql, {"post_id": post_id, "username":username})
        db.session.commit()
        post = result.fetchone()
        return post
    except:
        return False