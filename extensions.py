from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Instantiate extensions (but not app)
db = SQLAlchemy()
login_manager = LoginManager()
