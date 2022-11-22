from extensions import db, bcrypt
from app.accounts.role import Role


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    isBanned = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.TEXT, nullable=False)
    phone = db.Column(db.String(18), nullable=False, unique=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    role = db.Column(db.Enum(Role), nullable=False, default=Role.user)

    def has_role(self, roles) -> bool:
        for role in roles:
            if isinstance(role, Role):
                if self.role == role:
                    return True
            elif isinstance(role, str):
                if self.role.name == role:
                    return True
            elif isinstance(role, int):
                if self.role.value == role:
                    return True

        return False

    def check_password(self, password) -> bool:
        return bcrypt.check_password_hash(self.password, password)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def __repr__(self):
        return f"<User {self.id}>"


__all__ = ['User']
