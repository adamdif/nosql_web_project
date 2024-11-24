from flask import Flask

def create_app():
    app = Flask(__name__)

    # Enregistre les routes
    from app.routes import main
    app.register_blueprint(main)

    return app
