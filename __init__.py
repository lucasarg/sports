from flask import Flask
from config import DevelopmentConfig
from dotenv import load_dotenv
import os

from app.extensions import db, login_manager  # ✅ From extensions
from app.routes import register_routes        # ✅ Register all Blueprints

# Load environment variables from .env
load_dotenv()

# ----------------------------------------
# 🔧 Flask application factory
# ----------------------------------------
def create_app():
    app = Flask(__name__)

    # Load settings from config class
    app.config.from_object(DevelopmentConfig)

    # Set from environment (you can override DevelopmentConfig this way)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Default login route for @login_required
    login_manager.login_view = "auth.login"

    # ----------------------------------------
    # 🔁 User loader for Flask-Login
    # ----------------------------------------
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User  # ✅ Safe now
        return User.query.get(int(user_id))

    # ----------------------------------------
    # 📦 Register all blueprints
    # ----------------------------------------
    register_routes(app)

    return app
