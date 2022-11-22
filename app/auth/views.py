from datetime import datetime

from flask import request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_

from application import api
from extensions import db, bcrypt, jwt
from app.accounts.role import Role
from app.models import User, Location
from app.accounts.schemas.user import user_schema, users_schema


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


@api.route('/signup', methods=['POST'])
def signup():

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

        db.session.add(user)
        db.session.commit()

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'status': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': f'Could not save user'}), 500

    return jsonify({
        'data': user_schema.dump(user),
    })


@api.route('/login', methods=['POST'])
def login():

    if request.is_json:
        login = request.json['login']
        password = request.json['password']
    else:
        login = request.form['login']
        password = request.form['password']

    user = User.query.filter(
        or_(
            User.username == login,
            User.email == login
        )
    ).first()

    if not user:
        return jsonify(f"User with login {login} does not exists"), 404

    if user.check_password(password):
        access_token = create_access_token(identity=user)
        return jsonify(message='Login Successful', access_token=access_token)

    return jsonify("Wrong username or password"), 401

