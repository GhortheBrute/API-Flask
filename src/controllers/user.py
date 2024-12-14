from http import HTTPStatus
from flask import Blueprint, request, jsonify
from sqlalchemy import inspect
from src.app import User, db

app = Blueprint('user', __name__, url_prefix='/users')


def _create_user():
    data = request.json
    if not data or 'username' not in data:
        return {"error": "Invalid data"}, HTTPStatus.BAD_REQUEST

    user = User(username=data['username'])
    db.session.add(user)
    db.session.commit()


def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()

    if not users:
        return {"error": "No users"}

    return [
        {
            'id': user.id,
            'username': user.username
        }
        for user in users
    ]


@app.route('/', methods=['GET', 'POST'])
def handle_user():
    if request.method == 'POST':
        error = _create_user()
        if error:
            return jsonify(error), error[1]

        return {"message": "User successfully created"}, HTTPStatus.CREATED
    else:
        return {'users': _list_users()}


@app.route('/<int:user_id>')
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    return [
        {
            'id': user.id,
            'username': user.username
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
    db.session.delete(user)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT
