import os
from flask import Blueprint, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
from app.db_utils import init_mongo, init_postgres

main = Blueprint('main', __name__)

# Définir un dossier pour enregistrer les fichiers localement (optionnel)
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@main.route('/', methods=['GET'])
def form():
    return render_template('form.html')

@main.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username')
    email = request.form.get('email')
    file = request.files.get('file')  # Récupère le fichier téléchargé

    # Enregistre les données dans PostgreSQL
    try:
        conn = init_postgres()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, email) VALUES (%s, %s) RETURNING id", (username, email))
        user_id = cur.fetchone()[0]  # Récupère l'ID utilisateur
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        return f"Erreur PostgreSQL : {e}"

    # Gère le fichier et l'enregistre dans MongoDB
    if file:
        filename = secure_filename(file.filename)  # Nettoie le nom du fichier
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)  # Enregistre le fichier localement

        # Enregistre les métadonnées dans MongoDB
        try:
            db = init_mongo()
            db.documents.insert_one({
                "user_id": user_id,
                "username": username,
                "email": email,
                "file_name": filename,
                "file_path": file_path
            })
        except Exception as e:
            return f"Erreur MongoDB : {e}"

    return f"Données reçues et enregistrées pour {username}. Document associé : {filename if file else 'Aucun fichier'}"

@main.route('/users', methods=['GET'])
def list_users():
    users = []

    # Récupérer les utilisateurs de PostgreSQL
    try:
        conn = init_postgres()
        cur = conn.cursor()
        cur.execute("SELECT id, username, email FROM users;")
        postgres_users = cur.fetchall()  # [(id, username, email), ...]
        cur.close()
        conn.close()
    except Exception as e:
        return f"Erreur lors de la récupération des utilisateurs PostgreSQL : {e}"

    # Récupérer les documents associés dans MongoDB
    try:
        db = init_mongo()
        mongo_docs = list(db.documents.find())  # [{...}, {...}, ...]
    except Exception as e:
        return f"Erreur lors de la récupération des documents MongoDB : {e}"

    # Associer les utilisateurs PostgreSQL à leurs documents MongoDB
    for user in postgres_users:
        user_id, username, email = user
        document = next((doc for doc in mongo_docs if doc["user_id"] == user_id), None)
        users.append({
            "id": user_id,
            "username": username,
            "email": email,
            "document": document
        })

    # Rendre la page avec les données des utilisateurs
    return render_template('users.html', users=users)
