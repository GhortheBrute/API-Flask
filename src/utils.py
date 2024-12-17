from functools import wraps
from http import HTTPStatus

from flask_jwt_extended import get_jwt_identity

from app import User, db


def requires_role(role_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user = db.get_or_404(User, id=user_id)

            if user.role.name != role_name:
                return {'message': 'User does not have access.'}, HTTPStatus.FORBIDDEN
            return func(*args, **kwargs)

        return wrapper

    return decorator


def eleva_quadrado(x):
    return x ** 2
