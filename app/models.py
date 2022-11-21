from extensions import db


class Location(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    country = db.Column(db.String(200), nullable=False)
    region = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(200), nullable=False)
    street = db.Column(db.String(200), nullable=False)
    zip = db.Column(db.String(100))

    def __str__(self):
        return self.country + ' ' + self.city + ' ' + self.street

    def __repr__(self):
        return f"<Location {self.id}>"


from .accounts.models import *  # noqa
from .tags.models import *      # noqa
from .notices.models import *   # noqa
