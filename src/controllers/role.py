from http import HTTPStatus
from flask import Blueprint, request, jsonify

from app import Role, db

app = Blueprint('role', __name__, url_prefix='/roles')


@app.route('/', methods=['POST'])
def create_role():
    data = request.json
    role = Role(name=data['name'])
    db.session.add(role)
    db.session.commit()
    return {'message': 'Role successfully created'}, HTTPStatus.CREATED
