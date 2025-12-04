from flask import Flask, render_template, session, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash

from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, static_folder="dist")
app.secret_key = os.getenv("SECRET_KEY")

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
    if "user_id" not in session:
        return redirect(url_for("connexion"))
    return f"Bienvenue ! Vous êtes connecté. ID : {session['user_id']}"

@app.route("/inscription", methods=["GET", "POST"])
def inscription():
    if request.method == "POST":
        email = request.form["email"]
        mdp = request.form["mdp"]

        # Vérifie si l’utilisateur existe déjà
        existing_user = Utilisateur.query.filter_by(email=email).first()
        if existing_user:
            return "Cet email existe déjà."

        # Hash du mot de passe
        hashed = generate_password_hash(mdp)

        user = Utilisateur(email=email, mdp=hashed)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("connexion"))

    return render_template("inscription.html")


@app.route("/connexion", methods=["GET", "POST"])
def connexion():
    if request.method == "POST":
        email = request.form["email"]
        mdp = request.form["mdp"]

        user = Utilisateur.query.filter_by(email=email).first()
        if not user:
            return "Utilisateur introuvable."

        if not check_password_hash(user.mdp, mdp):
            return "Mot de passe incorrect."

        # Création de la session
        session["user_id"] = user.id

        return redirect(url_for("index"))

    return render_template("connexion.html")

@app.route("/deconnexion")
def deconnexion():
    if "user_id" in session:
        session.pop()
    return redirect(url_for("connexion"))

if __name__ == "__main__":
    app.run()