# ----------------------------------------
# 📦 Flask imports & app components
    # ----------------------------------------
from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from app.utils import login_required  # Custom decorator to protect routes
from app.models import User, Team, Player  # User model for session-based login
from app.forms import PlayerForm  # Form to create a player
from app.forms import TeamForm    # Form to create a team
from app import db  # Database instance

# ----------------------------------------
# 🔹 Create the main Blueprint
# ----------------------------------------
main = Blueprint('main', __name__)


# ----------------------------------------
# 🏠 Home page
# ----------------------------------------
@main.route('/')
def home():
    return render_template("index.html")


# ----------------------------------------
# 👤 Profile page (requires login)
# ----------------------------------------
@main.route('/profile')
@login_required  # Only accessible if the user is logged in
def profile():
    # Get the logged-in user using the session user_id
    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)


# ----------------------------------------
# 👥 Players section
# ----------------------------------------
from app.models import Player  # Player model
from flask import render_template  # (reimported, though already imported above — can be removed)

# View all players
@main.route("/players")
def view_players():
    team_id = request.args.get("team", type=int)
    search = request.args.get("search", "", type=str).strip().lower()

    teams = Team.query.order_by(Team.name).all()

    # Base query
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

# Add a new player (GET shows the form, POST handles the submission)
@main.route("/add-player", methods=["GET", "POST"])
def add_player():
    form = PlayerForm()  # Create an instance of the form
    if form.validate_on_submit():
        # Create a new player from form data
        new_player = Player(
            name=form.name.data,
            position=form.position.data,
            age=form.age.data,
            team_id = SelectField("Team", coerce=int)
        )
        db.session.add(new_player)  # Add player to database session
        db.session.commit()         # Commit changes to the database
        flash(f"Player {new_player.name} added successfully ✅", "success")  # Success message
        return redirect(url_for("main.view_players"))  # Redirect to players list

    # Show the form if GET or if validation fails
    return render_template("add_player.html", form=form)



@main.route("/edit-player/<int:id>", methods=["GET", "POST"])
def edit_player(id):
    player = Player.query.get_or_404(id)
    form = PlayerForm(obj=player)  # Carga los datos actuales

    # Cargar los equipos para el select
    form.team_id.choices = [(team.id, team.name) for team in Team.query.all()]

    if form.validate_on_submit():
        player.name = form.name.data
        player.position = form.position.data
        player.age = form.age.data
        player.team_id = form.team_id.data

        db.session.commit()
        flash(f"{player.name} updated successfully ✅", "success")
        return redirect(url_for("main.view_players"))

    return render_template("edit_player.html", form=form, player=player)



@main.route("/delete-player/<int:id>", methods=["POST"])
def delete_player(id):
    player = Player.query.get_or_404(id)
    db.session.delete(player)
    db.session.commit()
    flash(f"Player '{player.name}' deleted successfully 🗑️", "info")
    return redirect(url_for("main.view_players"))

@main.route("/players/<int:id>")
def player_detail(id):
    player = Player.query.get_or_404(id)
    return render_template("player_detail.html", player=player)


# ----------------------------------------
# 🏟️ Teams section
# ----------------------------------------
from app.models import Team  # Team model

# View all teams
@main.route("/teams")
def view_teams():
    teams = Team.query.all()  # Fetch all teams from the database
    return render_template("teams.html", teams=teams)

# Add a new team (GET shows the form, POST handles the submission)
@main.route("/add-team", methods=["GET", "POST"])
def add_team():
    form = TeamForm()  # Create an instance of the form
    if form.validate_on_submit():
        # Create a new team from form data
        new_team = Team(
            name=form.name.data,
            city=form.city.data
        )
        db.session.add(new_team)  # Add team to the session
        db.session.commit()       # Commit to database
        flash(f"Team {new_team.name} added successfully ✅", "success")  # Success message
        return redirect(url_for("main.view_teams"))  # Redirect to teams list
    
    # Show the form if GET or if validation fails
    return render_template("add_team.html", form=form)

@main.route("/edit-team/<int:id>", methods=["GET", "POST"])
def edit_team(id):
    team = Team.query.get_or_404(id)
    form = TeamForm(obj=team)
    if form.validate_on_submit():
        team.name = form.name.data
        team.city = form.city.data
        db.session.commit()
        flash(f"Team '{team.name}' updated ✏️", "success")
        return redirect(url_for("main.view_teams"))
    return render_template("edit_team.html", form=form, team=team)

@main.route("/delete-team/<int:id>", methods=["POST"])
def delete_team(id):
    team = Team.query.get_or_404(id)

    # Unassign team from all players
    players_to_delete = Player.query.filter_by(team_id=team.id).all()
    for player in players_to_delete:
        db.session.delete(player)

    db.session.delete(team)
    db.session.commit()
    flash(f"Team '{team.name}' deleted, and players unassigned ⚠️", "info")
    return redirect(url_for("main.view_teams"))

@main.route("/teams/<int:id>")
def team_detail(id):
    team = Team.query.get_or_404(id)
    players = Player.query.filter_by(team_id=team.id).all()
    return render_template("team_detail.html", team=team, players=players)
