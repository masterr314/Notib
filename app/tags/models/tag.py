from extensions import db


class Tag(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(30), nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Tag {self.id}>"


__all__ = ['Tag']
