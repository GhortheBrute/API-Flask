from http import HTTPStatus
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import inspect
from sqlalchemy.exc import SQLAlchemyError

from src.app import User, db
from src.utils import requires_role

app = Blueprint('user', __name__, url_prefix='/users')


def _create_user():
    data = request.json
    if not data or 'username' not in data:
        return {"error": "Invalid data"}, HTTPStatus.BAD_REQUEST

    user = User(
        username=data['username'],
        password=data['password'],
        role_id=data['role_id'],
    )
    try:
        db.session.add(user)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": str(e)}, HTTPStatus.BAD_REQUEST
    return {"message": "User successfully created"}, HTTPStatus.CREATED


def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()

    # if not users:
    #     return {"error": "No users"}

    return [
        {
            'id': user.id,
            'username': user.username,
            'role': {
                'id': user.role.id,
                'name': user.role.name,
            },
        }
        for user in users
    ]


@app.route('/', methods=['GET', 'POST'])
@jwt_required()
@requires_role("admin")
def handle_user():
    if request.method == 'POST':
        response, status_code = _create_user()
        return response, status_code
    else:
        return {'users': _list_users()}


@app.route('/<int:user_id>')
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    return [
        {
            'id': user.id,
            'username': user.username,
            'role': {
                'id': user.role.id,
                'name': user.role.name,
            }
        }
    ]


@app.route('/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    data = request.json

    if 'username' in data:
        user.username = data['username']
        db.session.commit()

    mapper = inspect(User)
    for column in mapper.attrs:
        if column.key in data:
            setattr(user, column.key, data[column.key])
    db.session.commit()

    return [
        {
            'id': user.id,
            'username': user.username
        }
    ]


@app.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    user.active = False
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT
