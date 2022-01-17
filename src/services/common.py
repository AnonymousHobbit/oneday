from flask import request, session, abort


def username():
    return session.get("username", None)

def id():
    return session.get("id", 0)


def csrf_check():
    if session.get("csrf", 0) != request.form["csrf_token"]:
        abort(403)


def role():
    return session.get("role", None)


def auth():
    if session.get("id", 0) > 0 and session.get("username", None) is not None:
        return True
    return False

def permissions(name, company_name=None):
    
    if session.get("username", None) not in [name, company_name]:
        abort(403)
    

