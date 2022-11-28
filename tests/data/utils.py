from extensions import db
from tests.data.data import (
    get_pseudo_real_groups,
    get_pseudo_real_users,
    get_test_user,
    get_pseudo_real_notices
)
from app.models import (
    User,
    Location,
    Notice,
    Group,
    Tag
)


def add_test_users(only_test=False, with_notices=False):
    """Add test users to db with their locations."""

    if only_test:
        users = [get_test_user()]
    else:
        users = get_pseudo_real_users()

    notices = None
    if with_notices:
        notices = get_pseudo_real_notices()

    for user in users:

        current = user

        location = current.get('location')

        if location:
            loc = Location(**location)

            db.session.merge(loc)
            db.session.commit()

            del current['location']

            current['location_id'] = loc.id
            _user = User(**current)

            db.session.merge(_user)
            db.session.commit()

            if notices:
                result = [notice for notice in notices if notice.get('username') == _user.username]
                for notice in result:

                    _notice = notice

                    locc = _notice.get('location')

                    if loc:
                        locc = Location(**locc)

                        db.session.merge(locc)
                        db.session.commit()

                        del _notice['location']
                        _notice['location_id'] = locc.id

                        del _notice['username']
                        _notice['user'] = _user.id

                        _notice = Notice(**_notice)
                        db.session.merge(_notice)
                        db.session.commit()


def add_test_groups():

    for g in get_pseudo_real_groups():

        current = g

        tags = current.get('tags')

        del current['tags']

        _g = Group(**current)

        db.session.add(_g)
        db.session.commit()

        if tags:
            for t in tags:
                current_tag = t

                current_tag['group'] = _g

                _tag = Tag(**current_tag)

                db.session.add(_tag)
                db.session.commit()
