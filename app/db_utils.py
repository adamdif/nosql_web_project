import psycopg2 # type: ignore
from pymongo import MongoClient

# Fonction pour connecter à PostgreSQL
def init_postgres():
    conn = psycopg2.connect(
        dbname="mydb",
        user="myuser",
        password="mypassword",
        host="postgres",  # Nom du conteneur PostgreSQL dans docker-compose.yml
        port="5432"
    )
    return conn

# Fonction pour connecter à MongoDB
def init_mongo():
    client = MongoClient("mongo", 27017)  # 'mongo' correspond au nom du conteneur MongoDB
    db = client['mydb']  # Nom de la base de données MongoDB
    return db
