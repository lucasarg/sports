from flask import Blueprint, render_template, redirect, url_for, flash, session
from app.models import User               # Model representing the 'users' table
from app import db                        # SQLAlchemy database instance
from werkzeug.security import generate_password_hash, check_password_hash  # For password encryption
from app.forms import LoginForm, RegisterForm  # Forms for login and registration

# ----------------------------------------
# 🔐 Blueprint for authentication routes
# ----------------------------------------
auth = Blueprint('auth', __name__)

# ----------------------------------------
# 🔑 Login route (GET shows the form, POST processes the login)
# ----------------------------------------
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data  # Get the entered username
        password = form.password.data  # Get the entered password

        # Search for the user in the database
        user = User.query.filter_by(username=username).first()

        # Check if user exists and password is correct
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id  # 🔐 This marks the user as "logged in"
            flash(f'Welcome {user.username} 👋', 'success')
            return redirect(url_for('main.home'))  # Redirect to the home page
        else:
            flash('Invalid credentials ❌', 'danger')  # Show error message

    # If GET request or form is not valid, show the login form again
    return render_template('login.html', form=form)

# ----------------------------------------
# 📝 Registration route (GET shows the form, POST registers the user)
# ----------------------------------------
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        # Hash the password before saving it
        hashed_password = generate_password_hash(password)

        # Create a new user instance
        new_user = User(username=username, email=email, password=hashed_password)

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)

# ----------------------------------------
# 🚪 Logout route
# ----------------------------------------
@auth.route('/logout')
def logout():
    # Remove the user_id from the session
    session.pop('user_id', None)
    flash('You have been logged out 👋', 'info')
    return redirect(url_for('auth.login'))
