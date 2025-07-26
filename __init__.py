from flask import Flask, session                    # <-- importado aquí
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig
from dotenv import load_dotenv
import os
load_dotenv()  # Carga el archivo .env

# Creamos la instancia de SQLAlchemy fuera de create_app para importarla en models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    

    # Configuración de la base de datos SQLite (archivo local)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


    # Inicializamos la base de datos con la app Flask
    db.init_app(app)

    # Registramos los blueprints
    from .routes import main
    from .auth.routes import auth
    app.register_blueprint(main)
    app.register_blueprint(auth)

    @app.context_processor
    def injectar_usuario_actual():
        from app.models import Usuario                      
        usuario = None
        if "usuario_id" in session:
            usuario = Usuario.query.get(session["usuario_id"])
        return dict(usuario_actual=usuario)

    return app
