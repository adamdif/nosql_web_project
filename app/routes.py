import os
from flask import Blueprint, render_template, request, send_from_directory, abort
from werkzeug.utils import secure_filename
from app.db_utils import init_mongo, init_postgres

main = Blueprint('main', __name__)

# Définir un dossier pour enregistrer les fichiers localement (optionnel)
UPLOAD_FOLDER = os.path.abspath('/app/uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@main.route('/', methods=['GET'])
def form():
    return render_template('form.html')

@main.route('/submit', methods=['GET', 'POST'])
def submit_user():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        file = request.files.get('file')  # Récupérer le fichier du formulaire

        # Sauvegarder l'utilisateur dans PostgreSQL
        try:
            conn = init_postgres()
            cur = conn.cursor()
            cur.execute("INSERT INTO users (username, email) VALUES (%s, %s) RETURNING id;", (username, email))
            user_id = cur.fetchone()[0]  # Récupère l'ID de l'utilisateur créé
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            return f"Erreur PostgreSQL : {e}"

        # Sauvegarder le fichier dans `uploads` si présent
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            # Enregistrer les métadonnées dans MongoDB
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

        return "Utilisateur et fichier ajoutés avec succès."

    return render_template('submit.html')

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

@main.route('/uploads/<filename>', methods=['GET'])
def download_file(filename):
    print(f"Flask cherche : ./uploads/{filename}")
    try:
        return send_from_directory('/app/uploads', filename, as_attachment=True)
    except FileNotFoundError:
        print(f"Erreur : fichier introuvable ./uploads/{filename}")
        abort(404, description="Fichier introuvable")
