
# Plateforme de Dépôt

Une plateforme simple et intuitive pour gérer les utilisateurs et leurs documents.

---

## Description
Ce projet est une application web construite avec **Flask** et **Docker**. Elle permet :
- D'ajouter des utilisateurs avec leurs informations et un fichier associé.
- De stocker les données des utilisateurs dans **PostgreSQL**.
- De sauvegarder les fichiers uploadés dans **MongoDB** (métadonnées) et un répertoire local.
- D'afficher une liste des utilisateurs et leurs fichiers.
- De télécharger les fichiers associés à chaque utilisateur.

---

## Fonctionnalités
1. **Ajout d'utilisateurs :**
   - Enregistrement des informations (nom, email) dans PostgreSQL.
   - Upload de fichiers et stockage des métadonnées dans MongoDB.

2. **Liste des utilisateurs :**
   - Affichage des utilisateurs avec leurs documents.
   - Option pour télécharger les fichiers.

3. **Recherche :**
   - Recherche d'utilisateurs par nom.

4. **Mode Développement :**
   - Changements en direct grâce au mode `FLASK_ENV=development`.

---

## Technologies Utilisées
- **Backend :** Flask (Python)
- **Base de données :** PostgreSQL et MongoDB
- **Frontend :** HTML, CSS
- **Conteneurisation :** Docker, Docker Compose

---

## Installation

### **Prérequis**
- **Docker** et **Docker Compose** installés.

### **Étapes**
1. Clonez ce dépôt :
   ```bash
   git clone <URL_DU_DEPOT>
   cd <NOM_DU_DEPOT>
   ```

2. Construisez et démarrez les conteneurs :
   ```bash
   docker-compose up --build
   ```

3. Accédez à l'application :
   - Frontend : [http://127.0.0.1:5000](http://127.0.0.1:5000)

4. Ajoutez un utilisateur ou affichez les utilisateurs.

---

## Structure du Projet
```
project/
├── app/
│   ├── templates/              # Fichiers HTML
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── submit.html
│   │   └── users.html
│   ├── static/                 # Fichiers CSS et autres
│   │   └── styles.css
│   ├── routes.py               # Routes Flask
│   ├── db_utils.py             # Fonctions pour PostgreSQL et MongoDB
├── uploads/                    # Dossier pour les fichiers uploadés
├── docker-compose.yml          # Configuration Docker Compose
├── Dockerfile                  # Configuration Docker Flask
├── requirements.txt            # Dépendances Python
└── README.md                   # Documentation
```

---

## Utilisation en Mode Développement
Pour activer le mode développement (avec rechargement automatique) :
1. Modifiez la variable d'environnement dans `docker-compose.yml` :
   ```yaml
   environment:
      FLASK_ENV: development
   ```

2. Relancez l'application :
   ```bash
   docker-compose up --build
   ```

---

## Bonnes Pratiques
- Les fichiers uploadés sont enregistrés dans le répertoire `uploads/`.
- Le répertoire `uploads/` est ignoré dans Git grâce à `.gitignore`.

---

## Contributions
Les contributions sont les bienvenues ! Suivez ces étapes :
1. Forkez le projet.
2. Créez une branche pour votre fonctionnalité :
   ```bash
   git checkout -b feature/ma-fonctionnalite
   ```
3. Faites un commit de vos modifications :
   ```bash
   git commit -m "Ajout de ma fonctionnalité"
   ```
4. Poussez vers votre dépôt forké :
   ```bash
   git push origin feature/ma-fonctionnalite
   ```
5. Créez une **Pull Request**.

---
