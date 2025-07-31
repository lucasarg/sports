from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import Player, Team
from app.forms import PlayerForm

player_bp = Blueprint("player", __name__)

@player_bp.route("/players")
def view_players():
    team_id = request.args.get("team", type=int)
    search = request.args.get("search", "", type=str).strip().lower()
    teams = Team.query.order_by(Team.name).all()
    query = Player.query

    if team_id:
        query = query.filter_by(team_id=team_id)

    if search:
        query = query.filter(
            db.or_(
                Player.name.ilike(f"%{search}%"),
                Player.position.ilike(f"%{search}%")
            )
        )

    players = query.all()
    return render_template("players.html", players=players, teams=teams, selected_team=team_id, search=search)


@player_bp.route("/add-player", methods=["GET", "POST"])
def add_player():
    form = PlayerForm()
    form.team_id.choices = [(team.id, team.name) for team in Team.query.all()]
    if form.validate_on_submit():
        new_player = Player(
            name=form.name.data,
            position=form.position.data,
            age=form.age.data,
            team_id=form.team_id.data
        )
        db.session.add(new_player)
        db.session.commit()
        flash(f"Player {new_player.name} added successfully ✅", "success")
        return redirect(url_for("player.view_players"))
    return render_template("add_player.html", form=form)


@player_bp.route("/edit-player/<int:id>", methods=["GET", "POST"])
def edit_player(id):
    player = Player.query.get_or_404(id)
    form = PlayerForm(obj=player)
    form.team_id.choices = [(team.id, team.name) for team in Team.query.all()]
    if form.validate_on_submit():
        player.name = form.name.data
        player.position = form.position.data
        player.age = form.age.data
        player.team_id = form.team_id.data
        db.session.commit()
        flash(f"{player.name} updated successfully ✅", "success")
        return redirect(url_for("player.view_players"))
    return render_template("edit_player.html", form=form, player=player)


@player_bp.route("/delete-player/<int:id>", methods=["POST"])
def delete_player(id):
    player = Player.query.get_or_404(id)
    db.session.delete(player)
    db.session.commit()
    flash(f"Player '{player.name}' deleted successfully 🗑️", "info")
    return redirect(url_for("player.view_players"))


@player_bp.route("/players/<int:id>")
def player_detail(id):
    player = Player.query.get_or_404(id)
    return render_template("player_detail.html", player=player)
