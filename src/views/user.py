from marshmallow import fields

from src.app import ma
from src.models.user import User
from src.views.role import RoleSchema


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        # fields = ("id", "username", "role_id")

    id = ma.auto_field()
    username = ma.auto_field()
    role = ma.Nested(RoleSchema)


class CreateUserSchema(ma.Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    role_id = fields.Integer(required=True)
