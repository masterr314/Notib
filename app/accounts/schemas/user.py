from app.models import User
from app.accounts.role import Role
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_enum import EnumField


class UserSchema(SQLAlchemyAutoSchema):

    role = EnumField(Role, by_value=True)

    class Meta:
        model = User
        load_instance = True


user_schema = UserSchema()
users_schema = UserSchema(many=True)
