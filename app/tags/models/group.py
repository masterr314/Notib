from extensions import db


class Group(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    tags = db.relationship('Tag', backref="group")

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Group {self.id}>'


__all__ = ['Group']
