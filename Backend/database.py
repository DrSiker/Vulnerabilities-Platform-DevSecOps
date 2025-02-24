from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Vulnerability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.text, nullable=False)
    severity = db.Column(db.String(50), nullable=False)