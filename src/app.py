import os
from datetime import datetime

import click
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, DateTime, func, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
jwt = JWTManager()


class Role(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    user: Mapped[list['User']] = relationship(back_populates="role")

    def __repr__(self) -> str:
        return f'Role(id={self.id!r}, role={self.name!r})'


class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    role_id: Mapped[int] = mapped_column(ForeignKey('role.id'))
    role: Mapped['Role'] = relationship(back_populates='user')

    def __repr__(self) -> str:
        return f'User(id={self.id!r}, username={self.username!r})'


class Post(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    body: Mapped[str] = mapped_column(String, nullable=False)
    created: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))

    def __repr__(self) -> str:
        return f'Post(id={self.id!r}, title={self.title!r}, author_id={self.author_id!r})'


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
        SQLALCHEMY_DATABASE_URI='sqlite:///blog.db',
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
