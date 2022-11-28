import json

from tests.base.base import Base
from tests.data.utils import add_test_groups
from app.models import Group, Tag


class TestGroupsViews(Base):

    def setUp(self):
        super(TestGroupsViews, self).setUp(login_test_user=True)
        add_test_groups()

    def test_get_groups(self):
        res = self.client.get(
            f'{self.API_PREFIX}/groups',
            headers=self.headers,
            content_type="application/json",
        )

        assert res.status_code == 200

        res = json.loads(res.data.decode()).get('data')

        groups = Group.query.all()

        assert isinstance(res, list)
        assert len(groups) == len(res) == 2

    def test_get_tags(self):
        res = self.client.get(
            f'{self.API_PREFIX}/tags',
            headers=self.headers,
            content_type="application/json",
        )

        assert res.status_code == 200

        res = json.loads(res.data.decode()).get('data')

        tags = Tag.query.all()

        assert isinstance(res, list)
        assert len(tags) == len(res) == 4

    def test_get_group_by_id(self):

        group = Group.query.filter(Group.name == 'Cars').first()

        res = self.client.get(
            f'{self.API_PREFIX}/group/{group.id}',
            headers=self.headers,
            content_type="application/json",
        )

        assert res.status_code == 200

        res = json.loads(res.data.decode()).get('data')

        assert isinstance(res, dict)
        assert group.name == res.get('name')
        assert group.description == res.get('description')

    def test_get_tag_by_id(self):
        tag = Tag.query.filter(Tag.id == 1).first()

        res = self.client.get(
            f'{self.API_PREFIX}/tag/{tag.id}',
            headers=self.headers,
            content_type="application/json",
        )

        assert res.status_code == 200

        res = json.loads(res.data.decode()).get('data')

        assert isinstance(res, dict)
        assert tag.name == res.get('name')
        assert tag.color == res.get('color')
        assert isinstance(tag.group, Group)

    def test_add_group(self):

        res = self.client.post(
            f'{self.API_PREFIX}/group',
            json={
                'name': 'Animals',
                'description': 'Notices about animals'
            },
            headers=self.headers,
            content_type="application/json",
        )

        assert res.status_code == 200

        res = json.loads(res.data.decode()).get('data')

        group = Group.query.filter_by(name='Animals').first()

        assert group
        assert group.name == res.get('name')
        assert group.description == res.get('description')

    def test_update_group(self):

        group = Group.query.filter(Group.name == 'Cars').first()

        res = self.client.put(
            f'{self.API_PREFIX}/group/{group.id}',
            json={
                'name': 'Tracks',
                'description': 'Notices about tracks'
            },
            headers=self.headers,
            content_type="application/json",
        )

        assert res.status_code == 200

        res = json.loads(res.data.decode()).get('data')

        group = Group.query.filter(Group.name == 'Cars').first()

        assert not group

        group = Group.query.filter(Group.name == 'Tracks').first()

        assert group.description == res.get('description')

    def test_delete_group(self):
        group = Group.query.filter(Group.name == 'Cars').first()

        res = self.client.delete(
            f'{self.API_PREFIX}/group/{group.id}',
            headers=self.headers,
        )

        assert res.status_code == 200

        res = json.loads(res.data.decode())

        assert res.get('status') == 'Group deleted'
        assert res.get('data').get('id') == group.id

        group = Group.query.filter(Group.name == 'Cars').first()

        assert not group

        groups = Group.query.all()

        assert len(groups) == 1

    def test_add_tag(self):

        group = Group.query.filter(Group.name == 'Cars').first()

        res = self.client.post(
            f'{self.API_PREFIX}/tag',
            json={
                'name': 'Tesla',
                'color': '#9741e8',
                'group_id': group.id
            },
            headers=self.headers,
            content_type="application/json",
        )

        assert res.status_code == 200

        res = json.loads(res.data.decode()).get('data')

        tag = Tag.query.filter_by(name='Tesla').first()

        assert tag
        assert tag.name == res.get('name')
        assert tag.color == res.get('color')
        assert tag.group.id == group.id

        tags = Tag.query.all()

        assert len(tags) == 5

    def test_add_tag_400(self):

        group = Group.query.filter(Group.name == 'Cars').first()

        res = self.client.post(
            f'{self.API_PREFIX}/tag',
            json={
                'name': None,
                'color': '#9741e8',
                'group_id': group.id
            },
            headers=self.headers,
            content_type="application/json",
        )

        assert res.status_code == 400
        assert res.status == '400 BAD REQUEST'

        tags = Tag.query.all()

        assert len(tags) == 4

    def test_add_group_400(self):
        res = self.client.post(
            f'{self.API_PREFIX}/group',
            json={
                'name': None,
                'description': 'Notices about animals'
            },
            headers=self.headers,
            content_type="application/json",
        )

        assert res.status_code == 400
        assert res.status == '400 BAD REQUEST'

        groups = Group.query.all()

        assert len(groups) == 2

    def test_update_tag(self):

        group = Group.query.filter(Group.name == 'Cars').first()
        tag = Tag.query.filter(Tag.name == 'Flat').first()

        res = self.client.put(
            f'{self.API_PREFIX}/tag/{tag.id}',
            json={
                'name': 'Tesla',
                'color': '#9741e8',
                'group_id': group.id
            },
            headers=self.headers,
            content_type="application/json",
        )

        assert res.status_code == 200

        res = json.loads(res.data.decode()).get('data')

        tag = Tag.query.filter(Tag.name == 'Flat').first()

        assert not tag

        tag = Tag.query.filter(Tag.name == 'Tesla').first()

        assert tag.name == res.get('name')
        assert tag.color == res.get('color')
        assert tag.group.id == group.id

    def test_delete_tag(self):

        tag = Tag.query.filter(Tag.name == 'Lexus').first()

        res = self.client.delete(
            f'{self.API_PREFIX}/tag/{tag.id}',
            headers=self.headers,
        )

        assert res.status_code == 200

        res = json.loads(res.data.decode())

        assert res.get('status') == 'Tag deleted'
        assert res.get('data').get('id') == tag.id

        tag = Tag.query.filter(Tag.name == 'Lexus').first()

        assert not tag

        tags = Tag.query.all()

        assert len(tags) == 3
