from flask import Blueprint, render_template, request
from app import init_postgres

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def form():
    return render_template('form.html')

@main.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username')
    email = request.form.get('email')

    # Connexion à PostgreSQL
    try:
        conn = init_postgres()
        cur = conn.cursor()

        # Insérer les données
        cur.execute("INSERT INTO users (username, email) VALUES (%s, %s)", (username, email))
        conn.commit()

        cur.close()
        conn.close()

        # Retourne une réponse
        return f"Données reçues et enregistrées : {username}, {email}"

    except Exception as e:
        print(f"Erreur lors de l'insertion dans PostgreSQL : {e}")
        return "Erreur lors de l'insertion des données."
