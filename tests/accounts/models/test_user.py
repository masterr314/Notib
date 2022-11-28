from datetime import datetime

from app.accounts.role import Role
from app.models import User, Location
from extensions import db, bcrypt
from tests.base.base import Base


class TestUser(Base):

    def test_user(self):

        location = Location(
            country='USA',
            region='California',
            city='Los Angeles',
            street='Reralys street 15',
        )
        db.session.merge(location)
        db.session.commit()

        user = User(
            username='rq23',
            first_name='Tom',
            last_name='Smith',
            birth_date=datetime.strptime('12-11-1997', "%d-%m-%Y"),
            email='tom_smith@gmail.com',
            password=bcrypt.generate_password_hash('1'),
            phone='1233445567',
            location_id=location.id,
        )

        db.session.add(user)
        db.session.commit()

        locations = Location.query.all()
        users = User.query.all()

        assert len(users) == 1

        user = users[0]

        assert isinstance(user, User)
        assert user.username == 'rq23'
        assert not user.has_role([Role.admin])
        assert user.has_role([Role.user])
        assert user.has_role(['user'])
        assert user.has_role([0])
        assert user.check_password('1')
        assert len(locations) == 1
        assert isinstance(locations[0], Location)
        assert locations[0].street == 'Reralys street 15'
        assert str(user) == user.first_name + ' ' + user.last_name
        assert repr(user) == f"<User {user.id}>"



