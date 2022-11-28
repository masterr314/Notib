import json

from tests.base.base import Base
from tests.data.utils import add_test_users
from app.models import User, Location
from extensions import bcrypt


class TestUserViews(Base):

    def setUp(self):
        super(TestUserViews, self).setUp(login_test_user=True)
        add_test_users()

    def test_get_users(self):

        res = self.client.get(
            f'{self.API_PREFIX}/users',
            headers=self.headers,
            content_type="application/json",
        )

        assert res.status_code == 200

        res = json.loads(res.data.decode()).get('data')

        users = User.query.all()

        assert isinstance(res, list)
        assert len(users) == len(res) == 3

    def test_get_user_by_id(self):
        res = self.client.get(
            f'{self.API_PREFIX}/user/2',
            headers=self.headers,
            content_type="application/json",
        )

        assert res.status_code == 200

        res = json.loads(res.data.decode()).get('data')

        assert isinstance(res, dict)
        assert res.get('username') == 'sam_smith'

    def test_add_user(self):
        res = self.client.post(
            f'{self.API_PREFIX}/user',
            json={
                "username": "bob_birgo",
                "first_name": "Bob",
                "last_name": "Birgo",
                "birth_date": '13-01-1989',
                "email": "bob_birgo@gmail.com",
                "password": '44445555',
                "phone": "9348590234",
                "location": {
                    "country": "German",
                    "region": "Beyer",
                    "city": "Munchen",
                    "street": "Hatsfte street 12"
                }
            },
            content_type="application/json",
        )

        assert res.status_code == 200

        res = json.loads(res.data.decode()).get('data')

        users = User.query.all()
        locations = Location.query.all()

        assert len(users) == len(locations) == 4
        assert isinstance(res, dict)

        user = User.query.filter(User.username == 'bob_birgo').first()
        location = Location.query.filter(Location.country == 'German').first()

        assert location and location.street == 'Hatsfte street 12'
        assert res.get('username') == 'bob_birgo' == user.username

    def test_add_user_400(self):
        res = self.client.post(
            f'{self.API_PREFIX}/user',
            json={
                "username": None,
                "first_name": "Bob",
                "last_name": "Birgo",
                "birth_date": '13-01-1989',
                "email": "bob_birgo@gmail.com",
                "password": '44445555',
                "phone": "9348590234",
                "location": {
                    "country": "German",
                    "region": "Beyer",
                    "city": "Munchen",
                    "street": "Hatsfte street 12"
                }
            },
            content_type="application/json",
        )

        assert res.status_code == 400
        assert res.status == '400 BAD REQUEST'

        users = User.query.all()

        assert len(users) == 3

    def test_update_user(self):

        user = User.query.filter_by(username='sam_smith').first()

        res = self.client.put(
            f'{self.API_PREFIX}/user/{user.id}',
            json={
                "username": "sam_smith2",
                "first_name": "Sam2",
                "last_name": "Smith2",
                "birth_date": '24-03-1998',
                "email": "sam_smith2@gmail.com",
                "isBanned": True,
                "old_password": "12345678",
                "password": "87654321",
                "phone": "111111111",
                "role": "admin",
            },
            content_type="application/json",
            headers=self.headers
        )

        assert res.status_code == 200

        res = json.loads(res.data.decode()).get('data')

        user = User.query.filter_by(username='sam_smith2').first()

        assert user
        assert user.username == res.get('username') == 'sam_smith2'
        assert user.email == res.get('email') == 'sam_smith2@gmail.com'
        assert user.isBanned and res.get('isBanned')
        assert bcrypt.check_password_hash(user.password, '87654321')
        assert user.phone == res.get('phone') == '111111111'

    def test_delete_user(self):

        user = User.query.filter_by(username='sam_smith').first()

        res = self.client.delete(
            f'{self.API_PREFIX}/user/{user.id}',
            headers=self.headers
        )

        assert res.status_code == 200

        res = json.loads(res.data.decode())

        assert res.get('status') == 'User deleted'
        assert res.get('data').get('id') == user.id

        user = User.query.filter_by(username='sam_smith').first()

        assert not user
