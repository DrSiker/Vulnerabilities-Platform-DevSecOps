from flask import Flask, render_template
import requests

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True  # Habilita la recarga automática de plantillas

BACKEND_URL = "http://vulnerabilities-platform-devsecops-backend-1:5000/vulnerabilities"

@app.route("/")
def index():
    try:
        response = requests.get(BACKEND_URL)
        vulnerabilities = response.json() if response.status_code == 200 else []
    except Exception as e:
        print("Error al obtener datos del backend:", e)
        vulnerabilities = []
    
    return render_template("index.html", vulnerabilities=vulnerabilities)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
