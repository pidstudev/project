import sqlite3
import click
from flask import current_app, g
from main.email_notifications import send_email_notification
from datetime import datetime, timedelta


def get_db():
    """
    This function is responsible for getting a database connection from the application context ('g').
    Checks if a database connextion exists in the application context.
    Otherwise creates a new connection to the SQLite database specified in the app config.
    """

    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )

        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """
    Closes the database connection stored in the application context ('g') if it exists.
    """

    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """
    Initializes the database by executing the SQL commands defined in schema.sql
    """

    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    # Schedule email notifications
    tomorrow = datetime.now() + timedelta(days=1)
    rentals = db.execute(
        "SELECT * FROM rentals WHERE email_notification_time = ?",
        (tomorrow,)
    ).fetchall()

    for rental in rentals:
        send_email_notification(rental['email'], 'Van Rental Notification', f'Your van rental is scheduled for {tomorrow}. Please prepare accordingly.')


@click.command('init-db')
def init_db_command():
    """
    Creates a CLI command 'init-db' that clears existing data and creates new tables in the db.
    """

    init_db()
    click.echo('Database initialized.')


def init_app(app):

    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)