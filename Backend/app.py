from flask import Flask, request, jsonify
from database import db, insert_vulnerabilities, get_vulnerabilities
from config_app import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

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
        {"id": v.id, "description": v.description, "severity": v.severity}
        for v in vulns
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)