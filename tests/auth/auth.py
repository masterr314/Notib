import json
from config import API_PREFIX


def register_user(self, data):
    return self.client.post(
        f"{API_PREFIX}/signup",
        data=json.dumps(data),
        content_type="application/json",
    )


def login_user(self, login, password):
    return self.client.post(
        f"{API_PREFIX}/login",
        data=json.dumps(
            dict(
                login=login,
                password=password,
            )
        ),
        content_type="application/json",
    )
