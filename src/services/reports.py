from __main__ import db
from flask import session

def create(title, domain, endpoint, description, severity, status, data):
    try:
        sql = "INSERT INTO reports (title, domain, endpoint, description, severity, status, company_name, user_name) values (:title, :domain, :endpoint, :description, :severity, :status, :company_name, :user_name)"
        db.session.execute(sql, {"title": title, "domain": domain, "endpoint": endpoint, "description": description, "severity": severity, "status": status, "company_name": data[1], "user_name": data[0]})
        db.session.commit()
        return True
    except:
        return False

def get_full(id):
    sql = "SELECT R.id, R.title, R.endpoint, R.severity, R.description, R.status, R.domain, C.name, TO_CHAR(R.date, 'dd / mm / yyyy'), C.username, R.user_name FROM reports R LEFT JOIN companies C ON R.company_name = C.username WHERE R.id=:id"
    result = db.session.execute(sql, {"id": id})
    report = result.fetchone()
    return report

def add_message(report_id, message):
    try:
        sql = "INSERT INTO messages (user_name, user_role, report_id, message) VALUES (:username, :user_role, :report_id, :message)"
        db.session.execute(sql, {"username": session["username"], "user_role": session["role"], "report_id": report_id, "message": message})
        db.session.commit()
        return True
    except:
        return False

def get_messages(report_id):
    sql = "SELECT user_name, user_role, TO_CHAR(date, 'MM / DD / YYYY, HH24:MI:SS'), message FROM messages WHERE report_id=:report_id"
    result = db.session.execute(sql, {"report_id": report_id})
    messages = result.fetchall()
    return messages

def close(report_id, status):
    try:
        sql = "UPDATE reports SET status=:status WHERE id=:report_id"
        db.session.execute(sql, {"status": status, "report_id": report_id})
        db.session.commit()
        return True
    except:
        return False

def latest(username):
    sql = "SELECT EXTRACT(HOUR FROM (NOW() - date)) FROM reports WHERE company_name=:username ORDER BY date DESC LIMIT 1"
    result = db.session.execute(sql, {"username": username})
    report = result.fetchone()
    return report

