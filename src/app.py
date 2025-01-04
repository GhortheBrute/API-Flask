import os

import click
from flask import Flask, current_app
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from src.models.models import db

migrate = Migrate()
jwt = JWTManager()


@click.command("init-db")
def init_db_command():
    """Clear the existing data e create new tables."""
    with current_app.app_context():
        db.create_all()
    click.echo("Initialized the database.")


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=os.environ['DATABASE_URL'],
        JWT_SECRET_KEY='super-secret',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register cli commands
    app.cli.add_command(init_db_command)

    # initializing extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # register Blueprint
    from src.controllers import user, post, auth, role

    app.register_blueprint(user.app)
    app.register_blueprint(post.app)
    app.register_blueprint(auth.app)
    app.register_blueprint(role.app)

    return app
