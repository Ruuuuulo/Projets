from flask import Flask, render_template, session, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix
from email_validator import validate_email, EmailNotValidError
import os
import re

app = Flask(__name__)

# Secret key obligatoire
app.secret_key = os.getenv("SECRET_KEY")
if not app.secret_key:
    raise RuntimeError("SECRET_KEY manquante !")

# Cookies sécurisés
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE="Lax"
)

# Limite requêtes
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024

# DB obligatoire
db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise RuntimeError("DATABASE_URL manquante !")
app.config["SQLALCHEMY_DATABASE_URI"] = db_url

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Force Flask à reconnaître HTTPS derrière Render
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

db = SQLAlchemy(app)

class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mdp = db.Column(db.String(255), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/inscription", methods=["GET", "POST"])
def inscription():
    if "user_id" in session:
        return redirect(url_for('index'))
    if request.method == "POST":

        # Validation email
        try:
            email = validate_email(request.form["email"]).normalized
        except EmailNotValidError:
            return render_template("inscription.html", message="L'email est invalide.")

        mdp = request.form["mdp"]
        mdp2 = request.form["mdp2"]
        if mdp != mdp2:
            return render_template("inscription.html", message="Les mots de passes doivent être identiques.")
        
        # Vérification du mot de passe
        pattern = (
            r'^(?=.*[A-Z])'         # 1 majuscule
            r'(?=.*\d)'             # 1 chiffre
            r'(?=.*[@$!%*?&;:.,/\\#^+=\-_<>{}()\[\]])'  # 1 spécial
            r'[A-Za-z\d@$!%*?&;:.,/\\#^+=\-_<>{}()\[\]]{8,}$'  # 8+ chars
        )

        if not re.match(pattern, mdp):
            return render_template("inscription.html", message="8 caractères min | 1 majuscule | 1 chiffre | 1 caractère spécial")

        # Vérifie si déjà inscrit
        existing_user = Utilisateur.query.filter_by(email=email).first()
        if existing_user:
            return render_template("inscription.html", message="L'email est déjà utilisé.")

        hashed = generate_password_hash(mdp, method="pbkdf2:sha256:260000")

        user = Utilisateur(email=email, mdp=hashed)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("connexion"))

    return render_template("inscription.html")

@app.route("/connexion", methods=["GET", "POST"])
def connexion():
    if "user_id" in session:
        return redirect(url_for('index'))
    if request.method == "POST":

        email = request.form["email"]
        mdp = request.form["mdp"]

        user = Utilisateur.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.mdp, mdp):
            return render_template("connexion.html", message="Identifiants invalides.")

        session["user_id"] = user.id
        return redirect(url_for("index"))

    return render_template("connexion.html")

@app.route("/deconnexion")
def deconnexion():
    session.pop("user_id", None)
    return redirect(url_for("connexion"))

@app.route("/defi1")
def defi1():
    return render_template("defi1.html")

@app.route("/quisommesnous")
def quisommesnous():
    return render_template("quisommesnous.html")

if __name__ == "__main__":
    app.run()

#BACKEND CODE PAR GABARRE CLAVERIA Santiago
