from flask import Flask, render_template, request
import requests

app = Flask(__name__)

BACKEND_URL = "http://backend:5000"

@app.route('/')
def index():
    """Carga las vulnerabilidades desde el backend"""
    severity = request.args.get("severity")
    order_by_severity = request.args.get("order_by_severity", "false")

    params = {"order_by_severity": order_by_severity}
    if severity:
        params["severity"] = severity

    try:
        response = requests.get(f"{BACKEND_URL}/vulnerabilities", params=params)
        vulnerabilities = response.json() if response.status_code == 200 else []
    except requests.exceptions.RequestException:
        vulnerabilities = []

    return render_template("index.html", vulnerabilities=vulnerabilities)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
