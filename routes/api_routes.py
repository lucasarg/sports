from flask import Blueprint, jsonify
from app.models import Player

api_bp = Blueprint("api", __name__)

@api_bp.route("/api/players")
def api_players():
    players = Player.query.all()
    data = [
        {
            "id": player.id,
            "name": player.name,
            "position": player.position,
            "age": player.age,
            "team": {
                "id": player.team.id,
                "name": player.team.name,
                "city": player.team.city
            } if player.team else None
        }
        for player in players
    ]
    return jsonify(data)


@api_bp.route("/api/players/<int:id>")
def api_player_detail(id):
    player = Player.query.get_or_404(id)
    data = {
        "id": player.id,
        "name": player.name,
        "position": player.position,
        "age": player.age,
        "team": {
            "id": player.team.id,
            "name": player.team.name,
            "city": player.team.city
        } if player.team else None
    }
    return jsonify(data)
