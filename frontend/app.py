from flask import Flask, render_template

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True  # 🔥 Habilita la recarga automática de plantillas

# Datos de ejemplo
vulnerabilities = [
    {"description": "SQL Injection", "severity": "Crítico"},
    {"description": "XSS", "severity": "Alto"},
    {"description": "CSRF", "severity": "Medio"},
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/vulnerabilities")
def vulnerabilities_view():
    return render_template("vulnerabilities.html", vulnerabilities=vulnerabilities)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
