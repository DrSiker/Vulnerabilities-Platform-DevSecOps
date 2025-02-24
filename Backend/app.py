from flask import Flask, request, jsonify
from database import db, Vulnerability
from config_app import Config
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app)

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Vulnerability Management Platform"}), 200

@app.route("/vulnerabilities", methods=["POST"])
def report_vulnerability():
    data = request.json
    
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON format. Expected a dictionary."}), 400
    
    vulnerabilities = []
    
    for key, value in data.items():
        if isinstance(value, list):  # Si es una lista de vulnerabilidades
            for item in value:
                description = item.get("description", "No description provided")
                severity = item.get("severity", "Unknown")
                vulnerabilities.append(Vulnerability(description=description, severity=severity))
        elif isinstance(value, dict):  # Si es un solo objeto
            description = value.get("description", "No description provided")
            severity = value.get("severity", "Unknown")
            vulnerabilities.append(Vulnerability(description=description, severity=severity))
    
    if not vulnerabilities:
        return jsonify({"error": "No valid vulnerabilities found in the request."}), 400

    db.session.add_all(vulnerabilities)
    db.session.commit()

    return jsonify({"message": f"{len(vulnerabilities)} vulnerabilities reported successfully"}), 201

@app.route("/vulnerabilities", methods=["GET"])
def get_vulnerabilities():
    vulnerabilities = Vulnerability.query.all()
    return jsonify([
        {"id": v.id, "description": v.description, "severity": v.severity}
        for v in vulnerabilities
    ])

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)