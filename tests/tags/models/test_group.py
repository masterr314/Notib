from app.models import Group, Tag
from extensions import db
from tests.base.base import Base


class TestGroup(Base):

    def test_group(self):

        group = Group(
            name="Cars",
            description="Buy, sell cars",
        )
        db.session.add(group)
        db.session.commit()

        tag = Tag(
            name='Suzuki',
            color='#32a852',
            group=group
        )
        db.session.add(tag)
        db.session.commit()

        groups = Group.query.all()
        tags = Tag.query.all()

        assert len(groups) == len(tags) == 1

        group = groups[0]
        tag = tags[0]

        assert isinstance(group, Group)
        assert group.name == 'Cars'
        assert group.description == 'Buy, sell cars'
        assert str(group) == group.name
        assert repr(group) == f"<Group {group.id}>"

        assert isinstance(tag, Tag)
        assert tag.name == 'Suzuki'
        assert tag.group.name == 'Cars'
        assert str(tag) == tag.name
        assert repr(tag) == f"<Tag {tag.id}>"
