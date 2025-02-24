import os
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_FILE = "vulnerable.db"

API_KEY = "sk_test_51H8KZ4RzzXEXAMPLE1234567890abcdef"
DB_PASSWORD = "SuperSecreto123!"

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


@app.route("/debug", methods=["GET"])
def debug():
    return jsonify({"environment": dict(os.environ)}) 


@app.route("/exec", methods=["POST"])
def exec_command():
    command = request.form["command"]
    output = os.popen(command).read() 
    return jsonify({"output": output})


@app.route("/redirect", methods=["GET"])
def open_redirect():
    url = request.args.get("url", "http://default.com")
    return f'<meta http-equiv="refresh" content="0; url={url}">'  
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
