from flask import Blueprint, render_template, session
from app.models import User
from app.utils import login_required

main = Blueprint("main", __name__)

@main.route('/')
def home():
    return render_template("index.html")

@main.route('/profile')
@login_required
def profile():
    user = User.query.get(session['user_id'])
    return render_template("profile.html", user=user)
