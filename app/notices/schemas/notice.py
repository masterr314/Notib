from app.models import Notice
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_enum import EnumField


class NoticeSchema(SQLAlchemyAutoSchema):

    type = EnumField(Notice, by_value=True)

    class Meta:
        model = Notice
        load_instance = True


notice_schema = NoticeSchema()
notices_schema = NoticeSchema(many=True)
