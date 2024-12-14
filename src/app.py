# app.py
from flask import Flask
from flask_login import LoginManager
from models import db, User, Transaction
from routes import api
from config import Config
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import logging
from logging.handlers import RotatingFileHandler, BaseRotatingHandler
import click
from flasgger import Swagger


app = Flask(__name__)

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}
swagger = Swagger(app, config=swagger_config)
app.config.from_object(Config)
db.init_app(app)

logging.basicConfig(level=logging.INFO)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'api.login_page'

from admin import admin
app.register_blueprint(admin)

app.register_blueprint(api, url_prefix='/api')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.cli.command('create_admin')
@click.option('--username', prompt='Username', help='The username of the admin.')
@click.option('--password', prompt='Password', hide_input=True, help='The password for the admin.')
def create_admin(username, password):
    """Create a default admin user."""
    with app.app_context():
        admin = User(username=username, password=password, role='admin')
        db.session.add(admin)
        db.session.commit()
        print(f"Admin user '{username}' created successfully.")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)