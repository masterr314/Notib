from datetime import datetime

from flask import request, jsonify
from sqlalchemy.exc import IntegrityError

from application import api
from app.models import User, Location
from app.accounts.schemas.user import user_schema, users_schema
from app.accounts.role import Role
from extensions import db, bcrypt


@api.route("/")
def root():
    return f'Main page'


@api.route("/hello-world-<int:variant>")
def hello_world(variant):
    return f'Hello World {variant}'


@api.route("/users")
def get_users():
    users = User.query.all()

    return jsonify({
        'data': users_schema.dump(users),
    })


@api.route('/user/<user_id>')
def get_user_by_id(user_id):
    user = User.query.filter(User.id == user_id).first()

    if not user:
        return jsonify({'status': f'User with {user_id} not found'}), 404

    return jsonify({
        'data': user_schema.dump(user),
    })


@api.route('/user', methods=['POST'])
def add_user():

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

        user = User(
            username=data.get('username'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            birth_date=datetime.strptime(data.get('birth_date', ''), "%d-%m-%Y"),
            email=data.get('email'),
            password=bcrypt.generate_password_hash(data.get('password')),
            phone=data.get('phone'),
            location_id=location.id,
            role=data.get('role') if data.get('role') else Role.user
        )

        db.session.merge(user)
        db.session.commit()

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'status': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': f'Could not save user'}), 500

    _user = User.query.filter(User.username == data.get('username')).first()

    return jsonify({
        'data': user_schema.dump(_user),
    })


@api.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):

    data = request.json

    user = User.query.filter(User.id == user_id).first()

    if not user:
        return jsonify({'status': 'No such user'}), 400

    if data.get('username'):
        user.username = data.get('username')

    if data.get('first_name'):
        user.first_name = data.get('first_name')

    if data.get('last_name'):
        user.last_name = data.get('last_name')

    if data.get('birth_date', ''):
        user.birth_date = datetime.strptime(data.get('birth_date', ''), "%d-%m-%Y")

    if data.get('isBanned'):
        user.isBanned = data.get('isBanned')

    if data.get('email'):
        user.email = data.get('email')

    if data.get('old_password') and bcrypt.check_password_hash(user.password, data.get('old_password')):
        user.password = bcrypt.generate_password_hash(data.get('password'))

    if data.get('phone'):
        user.phone = data.get('phone')

    if data.get('role'):
        user.role = Role[data.get('role')]

    try:
        db.session.merge(user)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'status': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'status': f'Could not save user'}), 500

    _user = User.query.filter(User.id == user_id).first()

    return jsonify({
        'data': user_schema.dump(_user),
    })


@api.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):

    user = User.query.filter(User.id == user_id).first()

    if not user:
        return jsonify({'status': 'No such user'}), 400

    try:
        db.session.delete(user)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'status': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'status': f'Could not delete user'}), 500

    return jsonify({
        'status': 'User deleted',
        'data': user_schema.dump(user),
    })

