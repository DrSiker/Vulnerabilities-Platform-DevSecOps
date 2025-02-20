from flask import Flask, request, jsonify
from database import db, Vulnerability
import os

app = Flask(__name__)
app.config.from_object("config.Config")

db.init_app(app)

@app.route('/vulnerabilities', methods=['POST'])
def report_vulnerability():
    data = request.json
    new_vuln = Vulnerability(description=data["description"], severity=data["severity"])
    db.session.add(new_vuln)
    db.session.commit()
    return jsonify({"message": "Vulnerability reported successfully"}), 201

@app.route('/vulnerabilities', methods=['GET'])
def get_vulnerabilities():
    vulnerabilities = Vulnerability.query.all()
    return jsonify([{ "id": v.id, "description": v.description, "severity": v.severity } for v in vulnerabilities])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
