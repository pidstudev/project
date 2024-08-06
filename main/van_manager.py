from flask import Blueprint, render_template, redirect, url_for, flash, request, g
from .db import get_db
from .auth import login_required
from main.email_notifications import send_email_notification
from datetime import datetime, timedelta


bp = Blueprint('van_manager', __name__, url_prefix='/van')


@bp.route('/', methods=['GET'])
@login_required
def index():
    """Display all rentals for the current user"""

    db = get_db()
    rentals = db.execute(
        'SELECT * FROM van_manager_app WHERE user_id = ? ORDER BY created DESC',
        (g.user['id'],)
    ).fetchall()

    return render_template('van_manager/rentals.html', rentals=rentals)


@bp.route('/rental/add', methods=['GET', 'POST'])
@login_required
def add_rental():
    """Add a new rental entry"""

    if request.method == 'POST':
        rental_data = request.form
        db = get_db()
        db.execute(
            """
            INSERT INTO van_manager_app
            (user_id, rental_date_from, rental_date_to, client_contact, pickup_location, destination, agreed_price)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                g.user['id'],
                rental_data['rental_date_from'],
                rental_data['rental_date_to'],
                rental_data['client_contact'],
                rental_data['pickup_location'],
                rental_data['destination'],
                rental_data['agreed_price']
            )
        )

        db.commit()

        # Schedule email notification
        tomorrow = datetime.now() + timedelta(days=1)
        send_email_notification(g.user['email'], 'Van Rental Notification', f'Your van rental is scheduled for {tomorrow}. Please prepare accordingly.')

        flash('Rental added successfully', 'success')

        return redirect(url_for('van_manager.index'))
    
    return render_template('van_manager/add_rental.html')


@bp.route('/rental/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_rental(id):
    """Update existing rental"""

    db = get_db()
    rental = db.execute(
        'SELECT * FROM van_manager_app WHERE id = ?', (id,)
    ).fetchone()

    if rental is None or rental['user_id'] != g.user['id']:
        flash('Rental not found', 'error')
        return redirect(url_for('van_manager.index'))
    
    if request.method == 'POST':
        rental_data = request.form
        db.execute(
            """
            UPDATE van_manager_app SET
            rental_date_from = ?,
            rental_date_to = ?,
            client_contact = ?,
            pickup_location = ?,
            destination = ?,
            agreed_price = ?
            WHERE id = ?
            """,
            (
                rental_data['rental_date_from'],
                rental_data['rental_date_to'],
                rental_data['client_contact'],
                rental_data['pickup_location'],
                rental_data['destination'],
                rental_data['agreed_price'],
                id
            )
        )

        db.commit()
        flash('Rental updated successfully', 'success')
        return redirect(url_for('van_manager.index'))
    
    return render_template('van_manager/update_rental.html', rental=rental)


@bp.route('/rental/<int:id>/delete', methods=['POST'])
@login_required
def delete_rental(id):
    """Delete an existing rental."""

    db = get_db()
    rental = db.execute(
        'SELECT * FROM van_manager_app WHERE id = ?', (id,)
    ).fetchone()

    if rental is None or rental['user_id'] != g.user['id']:
        flash('Rental not found', 'error')
    else:
        db.execute('DELETE FROM van_manager_app WHERE id = ?', (id,))
        db.commit()
        flash('Rental deleted successfully', 'success')

    return redirect(url_for('van_manager.index'))