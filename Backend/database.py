from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

class Vulnerabilities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(50), nullable=False)
    tool = db.Column(db.String(50), nullable=False)
    file_path = db.Column(db.Text, nullable=True)
    line_number = db.Column(db.Integer, nullable=True)
    date_found = db.Column(db.DateTime, server_default=db.func.now())
    status = db.Column(db.String(20), default="pending", nullable=False)

def insert_vulnerabilities(findings):
    """Inserta vulnerabilidades en la base de datos"""
    for f in findings:
        vuln = Vulnerabilities(
            description=f["description"],
            severity=f["severity"],
            tool=f["tool"],
            file_path=f.get("file_path"),
            line_number=f.get("line_number"),
            status=f.get("status", "pending")
        )
        db.session.add(vuln)

    db.session.commit()

def get_vulnerabilities(severity=None, order_by_severity=False):
    """Consulta vulnerabilidades con filtros opcionales"""
    query = db.session.query(Vulnerabilities)

    if severity:
        query = query.filter(Vulnerabilities.severity == severity)

    if order_by_severity:
        query = query.order_by(Vulnerabilities.severity.desc())

    return query.all()
