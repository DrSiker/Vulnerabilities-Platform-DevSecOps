from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Vulnerability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(50), nullable=False)

def insert_vulnerabilities(findings):
    """Inserta vulnerabilidades en la base de datos"""
    for f in findings:
        vuln = Vulnerability(
            description=f["description"],
            severity=f["severity"]
        )
        db.session.add(vuln)

    db.session.commit()

def get_vulnerabilities(tool=None, severity=None, order_by_severity=False):
    """Consulta vulnerabilidades con filtros opcionales"""
    query = db.session.query(Vulnerability)

    if severity:
        query = query.filter(Vulnerability.severity == severity)

    if order_by_severity:
        query = query.order_by(Vulnerability.severity.desc())

    return query.all()
