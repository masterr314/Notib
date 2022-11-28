import json

from tests.base.base import Base
from tests.data.utils import add_test_users
from app.models import User


class TestGroupsViews(Base):

    def setUp(self):
        super(TestGroupsViews, self).setUp()
        add_test_users()
        self.user = User.query.filter(User.username == 'sam_smith').first()
        self.password = '12345678'

    def test_login_ok_json(self):

        res = self.client.post(
            f'{self.API_PREFIX}/login',
            json={
                "login": self.user.username,
                "password": self.password,
            },
            content_type="application/json",
        )

        assert res.status_code == 200

        res = json.loads(res.data.decode())

        assert isinstance(res, dict)
        assert res.get('message') == 'Login Successful'
        assert res.get('access_token')

    def test_login_ok_form(self):

        res = self.client.post(
            f'{self.API_PREFIX}/login',
            data={
                "login": self.user.username,
                "password": self.password,
            },
        )

        assert res.status_code == 200

        res = json.loads(res.data.decode())

        assert isinstance(res, dict)
        assert res.get('message') == 'Login Successful'
        assert res.get('access_token')

    def test_login_404(self):

        login = self.user.username + '_no_such_user'
        res = self.client.post(
            f'{self.API_PREFIX}/login',
            json={
                "login": login,
                "password": self.password,
            },
            content_type="application/json",
        )

        assert res.status_code == 404

        res = res.data.decode()

        assert json.loads(res) == f'User with login {login} does not exists'

    def test_login_401(self):
        login = self.user.username
        res = self.client.post(
            f'{self.API_PREFIX}/login',
            json={
                "login": login,
                "password": self.password + '$',
            },
            content_type="application/json",
        )

        assert res.status_code == 401

        res = res.data.decode()

        assert json.loads(res) == 'Wrong username or password'
