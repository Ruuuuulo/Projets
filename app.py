from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Récupère l'URL depuis les variables d'environnement
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Table Utilisateur
class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mdp = db.Column(db.String(255), nullable=False)

# Crée les tables si elles n'existent pas
with app.app_context():
    db.create_all()
    print("La bd a été crée normalement.")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()