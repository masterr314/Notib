from app.models import Tag
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class TagSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = Tag
        load_instance = True


tag_schema = TagSchema()
tags_schema = TagSchema(many=True)
