from functools import wraps  # Import 'wraps' to preserve the original function's metadata
from flask import session, redirect, url_for, flash  # Flask tools for session handling, redirects, and flash messages

# This decorator is used to protect routes that require the user to be logged in
def login_required(f):
    @wraps(f)  # Ensures that the decorated function keeps its original name and docstring
    def decorated(*args, **kwargs):
        # Check if 'user_id' exists in the session, meaning the user is logged in
        if "user_id" not in session:
            # Show a warning message using Flask's flash system
            flash("You must log in first 🔐", "warning")
            # Redirect the user to the login page
            return redirect(url_for("auth.login"))
        
        # If the user is logged in, proceed with the original function
        return f(*args, **kwargs)

    # Return the wrapped (decorated) function
    return decorated
