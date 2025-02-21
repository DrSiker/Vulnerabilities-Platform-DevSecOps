from flask import Flask, request, jsonify
from database import db, Vulnerability
from backend.config_app import Config
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app)

@app.route("/vulnerabilities", methods=["POST"])
def report_vulnerability():
    data = request.json
    new_vuln = Vulnerability(description=data.get("description"), severity=data.get("severity"))
    db.session.add(new_vuln)
    db.session.commit()
    return jsonify({"message": "Vulnerability reported successfully"}), 201

@app.route("/vulnerabilities", methods=["GET"])
def get_vulnerabilities():
    vulnerabilities = Vulnerability.query.all()
    return jsonify([{ "id": v.id, "description": v.description, "severity": v.severity } for v in vulnerabilities])

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)