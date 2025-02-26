from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from config_app import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Modelo de Vulnerabilidades
class Vulnerabilities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(50), nullable=False)
    tool = db.Column(db.String(50))
    file_path = db.Column(db.Text)
    line_number = db.Column(db.Integer)
    date_found = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.String(50), default="pending")

# Función para insertar vulnerabilidades en la base de datos
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

# Función para obtener vulnerabilidades con filtros opcionales
def get_vulnerabilities(severity=None, order_by_severity=False):
    """Consulta vulnerabilidades con filtros opcionales"""
    query = db.session.query(Vulnerabilities)

    if severity:
        query = query.filter(Vulnerabilities.severity == severity)

    if order_by_severity:
        query = query.order_by(Vulnerabilities.severity.desc())

    return query.all()

# Diccionario de parsers por tipo de herramienta
from parsers.bandit_parser import parse_bandit
from parsers.snyk_parser import parse_snyk
from parsers.trivy_parser import parse_trivy
from parsers.gitleaks_parser import parse_gitleaks
from parsers.dependency_parser import parse_dependency_check

PARSERS = {
    "bandit": parse_bandit,
    "snyk": parse_snyk,
    "snyk_code": parse_snyk,
    "trivy": parse_trivy,
    "gitleaks": parse_gitleaks,
    "dependency-check": parse_dependency_check
}

@app.route('/upload-report', methods=['POST'])
def upload_report():
    """Recibe y procesa reportes JSON de seguridad"""
    report_type = request.args.get('type')
    data = request.get_json()

    if not report_type or report_type not in PARSERS:
        return jsonify({"error": "Invalid report type"}), 400

    findings = PARSERS[report_type](data)

    if not findings:
        return jsonify({"message": "No vulnerabilities found"}), 204

    insert_vulnerabilities(findings)
    return jsonify({"message": f"{report_type} report processed successfully"}), 201

@app.route('/vulnerabilities', methods=['GET'])
def get_vulns():
    """Consulta vulnerabilidades desde la base de datos"""
    severity = request.args.get("severity")
    order_by_severity = request.args.get("order_by_severity", "false").lower() == "true"

    vulns = get_vulnerabilities(severity=severity, order_by_severity=order_by_severity)

    return jsonify([
        {
            "id": v.id,
            "description": v.description,
            "severity": v.severity,
            "tool": v.tool,
            "file_path": v.file_path,
            "line_number": v.line_number,
            "date_found": v.date_found,
            "status": v.status
        }
        for v in vulns
    ])

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Asegurar que las tablas existen en la base de datos
    app.run(host="0.0.0.0", port=5000, debug=True)
