from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import Team, Player
from app.forms import TeamForm

team_bp = Blueprint("team", __name__)

@team_bp.route("/teams")
def view_teams():
    teams = Team.query.all()
    return render_template("teams.html", teams=teams)


@team_bp.route("/add-team", methods=["GET", "POST"])
def add_team():
    form = TeamForm()
    if form.validate_on_submit():
        new_team = Team(name=form.name.data, city=form.city.data)
        db.session.add(new_team)
        db.session.commit()
        flash(f"Team {new_team.name} added successfully ✅", "success")
        return redirect(url_for("team.view_teams"))
    return render_template("add_team.html", form=form)


@team_bp.route("/edit-team/<int:id>", methods=["GET", "POST"])
def edit_team(id):
    team = Team.query.get_or_404(id)
    form = TeamForm(obj=team)
    if form.validate_on_submit():
        team.name = form.name.data
        team.city = form.city.data
        db.session.commit()
        flash(f"Team '{team.name}' updated ✏️", "success")
        return redirect(url_for("team.view_teams"))
    return render_template("edit_team.html", form=form, team=team)


@team_bp.route("/delete-team/<int:id>", methods=["POST"])
def delete_team(id):
    team = Team.query.get_or_404(id)

    # ⚠️ Also delete all players in that team
    players_to_delete = Player.query.filter_by(team_id=team.id).all()
    for player in players_to_delete:
        db.session.delete(player)

    db.session.delete(team)
    db.session.commit()
    flash(f"Team '{team.name}' deleted, and its players removed ⚠️", "info")
    return redirect(url_for("team.view_teams"))


@team_bp.route("/teams/<int:id>")
def team_detail(id):
    team = Team.query.get_or_404(id)
    players = Player.query.filter_by(team_id=team.id).all()
    return render_template("team_detail.html", team=team, players=players)
