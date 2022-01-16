from __main__ import db

def create(title, endpoint, description, severity, status, data):
    try:
        sql = "INSERT INTO reports (title, endpoint, description, severity, status, company_name, user_name) values (:title, :endpoint, :description, :severity, :status, :company_name, :user_name)"
        db.session.execute(sql, {"title": title, "endpoint": endpoint, "description": description, "severity": severity, "status": status, "company_name": data[1], "user_name": data[0]})
        db.session.commit()
        return True
    except:
        return False

def get_full(id):
    sql = "SELECT R.id, R.title, R.endpoint, R.severity, R.description, R.status, C.name, TO_CHAR(NOW() :: DATE, 'dd / mm / yyyy') FROM reports R LEFT JOIN companies C ON R.company_name = C.username WHERE R.id=:id"
    result = db.session.execute(sql, {"id": id})
    report = result.fetchone()
    return report
