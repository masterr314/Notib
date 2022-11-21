from datetime import datetime

from extensions import db
from .notice_type import NoticeType


class Notice(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now())
    endAt = db.Column(db.DateTime)
    type = db.Column(db.Enum(NoticeType), nullable=False, default=NoticeType.public)
    user = db.Column(db.Integer, db.ForeignKey('user.id', primary_key=True))
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<Notice {self.id}>"


__all__ = ['Notice']
