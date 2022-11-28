import json

from app.notices.models.notice_type import NoticeType
from tests.base.base import Base
from tests.data.utils import add_test_users
from app.models import Notice, User, Location


class TestNoticeViews(Base):

    def setUp(self):
        super(TestNoticeViews, self).setUp(login_test_user=True)
        add_test_users(with_notices=True)

    def test_get_notices(self):
        res = self.client.get(
            f'{self.API_PREFIX}/notices',
            headers=self.headers,
            content_type="application/json",
        )

        assert res.status_code == 200

        res = json.loads(res.data.decode()).get('data')

        notices = Notice.query.all()

        assert isinstance(notices, list)
        assert len(notices) == len(res) == 2
        assert sorted([i.get('title') for i in res]) == sorted(['Sell car', 'Rent apartment'])

    def test_get_notice_by_id(self):
        res = self.client.get(
            f'{self.API_PREFIX}/notice/1',
            headers=self.headers,
            content_type="application/json",
        )

        assert res.status_code == 200

        res = json.loads(res.data.decode()).get('data')

        notice = Notice.query.filter(Notice.id == 1).first()

        assert isinstance(res, dict)
        assert notice.title == res.get('title')
        assert notice.text == res.get('text')

    def test_add_notice(self):
        res = self.client.post(
            f'{self.API_PREFIX}/notice',
            json={
                'title': 'Test Notice',
                'text': 'Test Notice Text',
                'endAt': '12-12-2023',
                "location": {
                    "country": "UK",
                    "region": "England",
                    "city": "Birmingem",
                    "street": "Mirgo street 56"
                },
            },
            headers=self.headers,
            content_type="application/json",
        )

        assert res.status_code == 200

        res = json.loads(res.data.decode()).get('data')

        notice = Notice.query.filter(Notice.title == 'Test Notice').first()

        test = User.query.filter(User.username == 'test').first()

        notices = Notice.query.all()

        assert isinstance(res, dict)
        assert notice.user == test.id
        assert len(notices) == 3
        assert notice.title == res.get('title') == 'Test Notice'
        assert notice.text == res.get('text') == 'Test Notice Text'

        location = Location.query.filter_by(street='Mirgo street 56').first()

        assert location.id == notice.location_id

    def test_add_notice_400(self):
        res = self.client.post(
            f'{self.API_PREFIX}/notice',
            json={
                'title': None,
                'text': 'Test Notice Text',
                'endAt': '12-12-2023',
                "location": {
                    "country": "UK",
                    "region": "England",
                    "city": "Birmingem",
                    "street": "Mirgo street 56"
                },
            },
            headers=self.headers,
            content_type="application/json",
        )

        assert res.status_code == 400
        assert res.status == '400 BAD REQUEST'

        notices = Notice.query.all()

        assert len(notices) == 2

    def test_update_notice(self):

        notice = Notice.query.filter(Notice.id == 1).first()

        res = self.client.put(
            f'{self.API_PREFIX}/notice/{notice.id}',
            json={
                'title': 'Test Notice 2',
                'text': 'Test Notice Text 2',
                'endAt': '12-12-2024',
                'type': 'private'
            },
            headers=self.headers,
            content_type="application/json",
        )

        assert res.status_code == 200

        res = json.loads(res.data.decode()).get('data')

        notice = Notice.query.filter(Notice.title == 'Test Notice 2').first()

        assert notice
        assert notice.title == res.get('title')
        assert notice.text == res.get('text')
        assert notice.type == NoticeType.private

    def test_delete_notice(self):

        notice = Notice.query.filter(Notice.id == 1).first()

        res = self.client.delete(
            f'{self.API_PREFIX}/notice/{notice.id}',
            headers=self.headers,
        )

        assert res.status_code == 200

        res = json.loads(res.data.decode())

        assert res.get('status') == 'Notice deleted'
        assert res.get('data').get('id') == notice.id

        notice = Notice.query.filter_by(id=1).first()

        assert not notice

        notices = Notice.query.all()
        assert len(notices) == 1
