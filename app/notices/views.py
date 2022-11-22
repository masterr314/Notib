from datetime import datetime

from flask import request, jsonify
from sqlalchemy.exc import IntegrityError

from application import api
from app.models import User, Location, Notice
from app.notices.schemas.notice import notice_schema, notices_schema
from extensions import db
from app.notices.models.notice_type import NoticeType
from app.auth.utils import grant_access


@api.route("/notices")
def get_notices():
    notices = Notice.query.all()

    return jsonify({
        'data': notices_schema.dump(notices),
    })


@api.route('/notice/<notice_id>')
def get_notice_by_id(notice_id):
    notice = Notice.query.filter(Notice.id == notice_id).first()

    if not notice:
        return jsonify({'status': f'User with {notice} not found'}), 404

    return jsonify({
        'data': notice_schema.dump(notice),
    })


@api.route('/notice', methods=['POST'])
@grant_access()
def add_notice():

    data = request.json

    try:

        if isinstance(data.get('location'), dict):
            loc = data.get('location')
            location = Location(
                country=loc.get('country'),
                region=loc.get('region'),
                city=loc.get('city'),
                street=loc.get('street'),
                zip=loc.get('region'),
            )
            db.session.merge(location)
            db.session.commit()
        else:
            location = data.get('location')

        notice = Notice(
            title=data.get('title'),
            text=data.get('text'),
            endAt=datetime.strptime(data.get('endAt', ''), "%d-%m-%Y"),
            type=data.get('type') if data.get('type') else NoticeType.public,
            location_id=location.id,
        )

        notice.createdAt = datetime.now()

        db.session.add(notice)
        db.session.commit()

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'status': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': f'Could not save user'}), 500

    return jsonify({
        'data': notice_schema.dump(notice),
    })


@api.route('/notice/<notice_id>', methods=['PUT'])
@grant_access()
def update_notice(notice_id):

    data = request.json

    notice = Notice.query.filter(Notice.id == notice_id).first()

    if not notice:
        return jsonify({'status': 'No such notice'}), 400

    if data.get('title'):
        notice.title = data.get('title')

    if data.get('text'):
        notice.text = data.get('text')

    if data.get('endAt'):
        notice.birth_date = datetime.strptime(data.get('endAt', ''), "%d-%m-%Y")

    if data.get('type'):
        notice.type = NoticeType[data.get('type')]

    try:
        db.session.add(notice)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'status': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'status': f'Could not save user'}), 500

    return jsonify({
        'data': notice_schema.dump(notice),
    })


@api.route('/notice/<notice_id>', methods=['DELETE'])
@grant_access()
def delete_notice(notice_id):

    notice = Notice.query.filter(Notice.id == notice_id).first()

    if not notice:
        return jsonify({'status': 'No such notice'}), 400

    try:
        db.session.delete(notice)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'status': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'status': f'Could not delete user'}), 500

    return jsonify({
        'status': 'Notice deleted',
        'data': notice_schema.dump(notice),
    })

