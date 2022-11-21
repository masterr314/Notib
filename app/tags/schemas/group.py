from app.models import Group
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class GroupSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = Group
        load_instance = True


group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)
