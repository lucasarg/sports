# ----------------------------------------
# 📦 Flask imports & app components
# ----------------------------------------
from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from app.utils import login_required  # Custom decorator to protect routes
from app.models import User  # User model for session-based login
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
    players = Player.query.all()  # Fetch all players from the database
    return render_template("players.html", players=players)

# Add a new player (GET shows the form, POST handles the submission)
@main.route("/add-player", methods=["GET", "POST"])
def add_player():
    form = PlayerForm()  # Create an instance of the form
    if form.validate_on_submit():
        # Create a new player from form data
        new_player = Player(
            name=form.name.data,
            position=form.position.data,
            age=form.age.data
        )
        db.session.add(new_player)  # Add player to database session
        db.session.commit()         # Commit changes to the database
        flash(f"Player {new_player.name} added successfully ✅", "success")  # Success message
        return redirect(url_for("main.view_players"))  # Redirect to players list

    # Show the form if GET or if validation fails
    return render_template("add_player.html", form=form)


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
