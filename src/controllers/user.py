import logging
from http import HTTPStatus

from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy import inspect
from sqlalchemy.exc import SQLAlchemyError

from src.app import bcrypt
from src.models import User, db
from src.views.user import UserSchema, CreateUserSchema

app = Blueprint("user", __name__, url_prefix="/users")


def _create_user():
    # data = request.json
    # if not data or "username" not in data:
    #     return {"error": "Invalid data"}, HTTPStatus.BAD_REQUEST

    user_schema = CreateUserSchema()
    try:
        data = user_schema.load(request.json)
    except ValidationError as e:
        return e.messages, HTTPStatus.UNPROCESSABLE_ENTITY

    user = User(
        username=data["username"],
        password=bcrypt.generate_password_hash(data["password"]),
        role_id=data["role_id"],
    )
    try:
        db.session.add(user)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": str(e)}, HTTPStatus.BAD_REQUEST
    return {"message": "User successfully created"}, HTTPStatus.CREATED


def _list_users():
    # logging.debug("Executing user query...")  # Debug print
    query = db.select(User)
    users = db.session.execute(query).scalars()
    # logging.debug(f"Query executed. Users found: {users}")  # Debug print

    if not users:
        return {"error": "No users"}, HTTPStatus.NO_CONTENT

    users_schema = UserSchema(many=True)
    users_list = users_schema.dump(users)

    # users_list = [
    #     {
    #         "id": user.id,
    #         "username": user.username,
    #         "role": {
    #             "id": user.role.id,
    #             "name": user.role.name,
    #         },
    #     }
    #     for user in users
    # ]
    # logging.debug(f"Users list constructed: {users_list}")  # Debug print
    return {"users": users_list}, HTTPStatus.OK


@app.route("/", methods=["GET", "POST"])
# @jwt_required()
# @requires_role("admin")
def handle_user():
    if request.method == "POST":
        users_response, status_code = _create_user()
        return users_response, status_code

    else:
        users_response, status_code = _list_users()
        logging.debug(
            f"Users response: {users_response}, Status code: {status_code}"
        )  # Debug print
        return users_response, status_code


@app.route("/<int:user_id>")
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    return jsonify({"id": user.id, "username": user.username})


@app.route("/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    data = request.json

    if "username" in data:
        user.username = data["username"]
        db.session.commit()

    mapper = inspect(User)
    for column in mapper.attrs:
        if column.key in data:
            setattr(user, column.key, data[column.key])
    db.session.commit()

    return [{"id": user.id, "username": user.username}]


@app.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT
