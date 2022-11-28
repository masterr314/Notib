from datetime import datetime

from app.models import Notice, Location
from extensions import db
from tests.base.base import Base


class TestNotice(Base):

    def test_notice(self):

        location = Location(
            country='USA',
            region='California',
            city='Los Angeles',
            street='Reralys street 15',
        )
        db.session.merge(location)
        db.session.commit()

        notice = Notice(
            title='Test Notice Title',
            text='Test Notice Text',
            endAt=datetime.strptime('11-11-2023', "%d-%m-%Y"),
            location_id=location.id,
        )

        db.session.add(notice)
        db.session.commit()

        locations = Location.query.all()
        notices = Notice.query.all()

        assert len(notices) == 1

        notice = notices[0]

        assert isinstance(notice, Notice)
        assert notice.title == 'Test Notice Title'
        assert len(locations) == 1
        assert isinstance(locations[0], Location)
        assert locations[0].street == 'Reralys street 15'
        assert str(notice) == notice.title
        assert repr(notice) == f"<Notice {notice.id}>"

