import os

from flask import Flask, render_template
from flask_mail import Mail

from dotenv import load_dotenv

load_dotenv()
mail = Mail()

# Factory function
def create_app(test_config=None):
    
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'main.sqlite'),
        # Configure Flask-Mail
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
        MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
        MAIL_PASSWORD=os.getenv('MAIL_PASSWORD')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        """Render the landing page"""
        return render_template('index.html')
    

    # Import and call db function from factory
    from . import db
    db.init_app(app)

    # Import and register blueprint from factory
    from . import auth
    app.register_blueprint(auth.bp)

    # Import and register van_manager blueprint
    from . import van_manager
    app.register_blueprint(van_manager.bp)
    
    return app