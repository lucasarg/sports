from .main_routes import main
from .player_routes import player_bp
from .team_routes import team_bp
from .api_routes import api_bp
from app.auth.routes import auth

def register_routes(app):
    app.register_blueprint(main)
    app.register_blueprint(player_bp)
    app.register_blueprint(team_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(auth)
