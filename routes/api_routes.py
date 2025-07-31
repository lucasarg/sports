# app/routes/api_routes.py
from flask import Blueprint, jsonify, request
from app.models import Player, Team
from app import db

api_bp = Blueprint('api', __name__)  # Blueprint is named 'api'

# ------------------------
# GET all players
# ------------------------
@api_bp.route("/api/players")
def api_players():
    players = Player.query.all()
    data = []
    for player in players:
        data.append({
            "id": player.id,
            "name": player.name,
            "position": player.position,
            "age": player.age,
            "team": {
                "id": player.team.id,
                "name": player.team.name,
                "city": player.team.city
            } if player.team else None
        })
    return jsonify(data)

# ------------------------
# GET one player by ID
# ------------------------
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

# ------------------------
# POST new player
# ------------------------
@api_bp.route("/api/players", methods=["POST"])
def api_create_player():
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"error": "Missing player name"}), 400

    player = Player(
        name=data["name"],
        position=data.get("position"),
        age=data.get("age"),
        team_id=data.get("team_id")
    )
    db.session.add(player)
    db.session.commit()

    return jsonify({
        "message": "Player created successfully",
        "player": {
            "id": player.id,
            "name": player.name,
            "position": player.position,
            "age": player.age,
            "team_id": player.team_id
        }
    }), 201

# ------------------------
# PUT update player by ID
# ------------------------
@api_bp.route("/api/players/<int:id>", methods=["PUT"])
def api_update_player(id):
    player = Player.query.get_or_404(id)
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    player.name = data.get("name", player.name)
    player.position = data.get("position", player.position)
    player.age = data.get("age", player.age)
    player.team_id = data.get("team_id", player.team_id)

    db.session.commit()

    return jsonify({
        "message": "Player updated successfully",
        "player": {
            "id": player.id,
            "name": player.name,
            "position": player.position,
            "age": player.age,
            "team_id": player.team_id
        }
    })

# ------------------------
# DELETE player by ID
# ------------------------
@api_bp.route("/api/players/<int:id>", methods=["DELETE"])
def api_delete_player(id):
    player = Player.query.get_or_404(id)
    db.session.delete(player)
    db.session.commit()
    return jsonify({"message": f"Player {player.name} deleted successfully."})

# Ensure the blueprint is exported
__all__ = ['api_bp']
