from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import DevelopmentConfig
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Instantiate extensions globally
db = SQLAlchemy()
login_manager = LoginManager()

# ----------------------------------------
# 🔧 Flask application factory
# ----------------------------------------
def create_app():
    app = Flask(__name__)

    # Load configuration from a class (DevelopmentConfig)
    app.config.from_object(DevelopmentConfig)

    # Set database connection using environment variable
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Set the secret key used for session, CSRF protection, etc.
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Initialize extensions with the Flask app
    db.init_app(app)
    login_manager.init_app(app)

    # Define the default login view if user tries to access a protected page
    login_manager.login_view = "auth.login"

    # ----------------------------------------
    # 🔁 User loader for Flask-Login
    # ----------------------------------------
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User  # Import here to avoid circular imports
        return User.query.get(int(user_id))

    # ----------------------------------------
    # 📦 Register blueprints (modular routes)
    # ----------------------------------------
    from .routes import main
    from .auth.routes import auth
    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app
