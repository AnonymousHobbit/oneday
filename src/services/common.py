from flask import request, session


def username():
    return session.get("username", None)

def id():
    return session.get("id", 0)


def csrf():
    if session.get("csrf", 0) == request.form["csrf"]:
        return True
    return False


def role():
    return session.get("role", None)


def auth():
    if session.get("id", 0) > 0 and session.get("username", None) is not None:
        return True
    return False
