import json
from unittest import TestCase

from extensions import db
from application import create_app
from tests.data.utils import add_test_users
from tests.data.data.users import get_test_user_credentials
from tests.auth.auth import login_user
from config import API_PREFIX, API_VERSION


class Base(TestCase):

    headers = {'Authorization': 'Bearer: test_token'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = create_app(config_mode='test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.API_PREFIX = API_PREFIX
        self.API_VERSION = API_VERSION

    def setUp(self, *args, **kwargs):
        db.create_all()
        if kwargs.get('login_test_user', None):
            self.login_test_user()

    def tearDown(self, *args, **kwargs):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login_test_user(self):
        add_test_users(only_test=True)
        credentials = get_test_user_credentials()
        result = login_user(
            self=self,
            login=credentials.get('username'),
            password=credentials.get('password'),
        )
        result = json.loads(result.data.decode())
        self.access_token = result.get("access_token")
        self.headers = {'Authorization': f'Bearer {self.access_token}'}
