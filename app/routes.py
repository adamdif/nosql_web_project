from flask import Blueprint, render_template, request

# Déclaration d’un blueprint pour regrouper les routes
main = Blueprint('main', __name__)

# Route pour afficher le formulaire
@main.route('/', methods=['GET'])
def form():
    return render_template('form.html')

# Route pour traiter les données soumises
@main.route('/submit', methods=['POST'])
def submit():
    # Récupère les données du formulaire
    username = request.form.get('username')
    email = request.form.get('email')

    # Logique pour enregistrer dans les bases de données (à faire plus tard)
    print(f"Nom d'utilisateur : {username}, Email : {email}")

    return f"Données reçues : {username}, {email}"
