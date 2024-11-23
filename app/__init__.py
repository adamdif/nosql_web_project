from flask import Flask
import psycopg2

def create_app():
    app = Flask(__name__)

    # Enregistre les routes
    from app.routes import main
    app.register_blueprint(main)

    return app

def init_postgres():
    conn = psycopg2.connect(
        dbname="mydb",
        user="myuser",
        password="mypassword",
        host="postgres",  # Nom du conteneur PostgreSQL
        port="5432"
    )
    return conn
