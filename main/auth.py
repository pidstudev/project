import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from main.db import get_db
from main.email_notifications import send_email_notification
from datetime import datetime, timedelta

bp = Blueprint('auth', __name__, url_prefix='/auth')

# ---------- REGISTER VIEW ----------
@bp.route('/register', methods=('GET', 'POST'))
def register():
    """
    Handles user registration by validating the form input, hashing the password, and inserting the user into the database.
    Redirects to the login page upon successful registration.
    """

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        email = request.form['email']
        phone_number = request.form.get('phone_number')

        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif password != confirm_password:
            error = 'Passwords do not match.'
        elif not email:
            error = 'Email is required.'

        if error is None:
            try:
                hashed_password = generate_password_hash(password)
                db.execute(
                    "INSERT INTO user (username, password, email, phone_number) VALUES (?, ?, ?, ?)",
                    (username, hashed_password, email, phone_number),
                )
                db.commit()

                # Schedule welcome email notification
                send_email_notification(email, 'Welcome to Van Rental Manager!', 
                    f'Hello {username},\n\nThank you for registering with Van Rental Manager. We are excited to have you onboard!\n\nBest regards,\nLakbayPinas')
                
                return redirect(url_for("auth.login"))

            except db.IntegrityError as e:
                error = f"User {username} is already registered or taken."
            
        flash(error)

    return render_template('auth/register.html')

# ---------- LOGIN VIEW ----------
@bp.route('/login', methods=('GET', 'POST'))
def login():
    """
    Handles user login by verifying the username and password against the database records.
    Stores the user's ID in the session upon successful login.
    Redirects to the index page upon successful login.
    """

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            
            # Optionally, send a login notification email
            send_email_notification(user['email'], 'Login Notification', 
                'Hello,\n\nYou have successfully logged in to your Van Rental Manager account.\n\nBest regards,\nLakbayPinas')
            
            return redirect(url_for('van_manager.index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    """
    Runs before each request to check if a user is logged in by retrieving the user's ID from the session.
    Retrieves the user's data from the database and stores it in g.user if the user is logged in.
    """

    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    """
    Clears the session upon user logout and redirects to the login page.
    """

    session.clear()
    return redirect(url_for('auth.login'))

# Require authentication in other views
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        """
        Checks if a user is loaded and redirects to the login page otherwise. If a user is loaded the original view is called and continues normally.
        """

        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view
