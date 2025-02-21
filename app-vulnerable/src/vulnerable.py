import os
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_FILE = "vulnerable.db"

# 🔴 Vulnerabilidad: SQL Injection
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    connection.close()
    if user:
        return jsonify({"message": "Login successful"})
    return jsonify({"message": "Invalid credentials"}), 401

# 🔴 Vulnerabilidad: Exposición de Información Sensible
@app.route("/debug", methods=["GET"])
def debug():
    return jsonify({"environment": dict(os.environ)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
