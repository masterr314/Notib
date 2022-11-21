from flask import request, jsonify
from sqlalchemy.exc import IntegrityError

from application import api
from app.models import Group, Tag
from app.tags.schemas.group import group_schema, groups_schema
from app.tags.schemas.tag import tag_schema, tags_schema
from extensions import db


@api.route("/groups")
def get_groups():
    groups = Group.query.all()

    return jsonify({
        'data': groups_schema.dump(groups),
    })


@api.route("/tags")
def get_tags():
    tags = Tag.query.all()

    return jsonify({
        'data': tags_schema.dump(tags),
    })


@api.route('/group/<group_id>')
def get_group_by_id(group_id):
    user = Group.query.filter(Group.id == group_id).first()

    if not user:
        return jsonify({'status': f'Group with {group_id} not found'}), 404

    return jsonify({
        'data': group_schema.dump(user),
    })


@api.route('/tag/<tag_id>')
def get_tag_by_id(tag_id):
    tag = Tag.query.filter(Tag.id == tag_id).first()

    if not tag:
        return jsonify({'status': f'Tag with {tag_id} not found'}), 404

    return jsonify({
        'data': tag_schema.dump(tag),
    })


@api.route('/tag', methods=['POST'])
def add_tag():

    data = request.json

    try:
        tag = Tag(
            name=data.get('name'),
            color=data.get('color'),
            group=Group.query.filter(Group.id == data.get('group_id')).first()
        )

        db.session.add(tag)
        db.session.commit()

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'status': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': f'Could not save tag'}), 500

    return jsonify({
        'data': tag_schema.dump(tag),
    })


@api.route('/tag/<tag_id>', methods=['PUT'])
def update_tag(tag_id):

    data = request.json

    tag = Tag.query.filter(Tag.id == tag_id).first()

    if not tag:
        return jsonify({'status': 'No such tag'}), 400

    if data.get('name'):
        tag.name = data.get('name')

    if data.get('color'):
        tag.description = data.get('color')

    if data.get('group_id'):
        tag.group = Group.query.filter(Group.id == data.get('group_id')).first()

    try:
        db.session.merge(tag)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'status': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': f'Could not update tag'}), 500

    tag = Tag.query.filter(Tag.id == tag_id).first()

    return jsonify({
        'data': tag_schema.dump(tag),
    })


@api.route('/tag/<tag_id>', methods=['DELETE'])
def delete_tag(tag_id):

    tag = Tag.query.filter(Tag.id == tag_id).first()

    if not tag:
        return jsonify({'status': 'No such group'}), 404

    try:
        db.session.delete(tag)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'status': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'status': f'Could not delete tag'}), 500

    return jsonify({
        'status': 'Tag deleted',
        'data': tag_schema.dump(tag),
    })


@api.route('/group', methods=['POST'])
def add_group():

    data = request.json

    try:
        group = Group(
            name=data.get('name'),
            description=data.get('description'),
        )

        db.session.add(group)
        db.session.commit()

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'status': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': f'Could not save group'}), 500

    return jsonify({
        'data': group_schema.dump(group),
    })


@api.route('/group/<group_id>', methods=['PUT'])
def update_group(group_id):

    data = request.json

    group = Group.query.filter(Group.id == group_id).first()

    if not group:
        return jsonify({'status': 'No such group'}), 404

    if data.get('name'):
        group.name = data.get('name')

    if data.get('description'):
        group.description = data.get('description')

    try:
        db.session.merge(group)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'status': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': f'Could not update group'}), 500

    group = Group.query.filter(Group.id == group_id).first()

    return jsonify({
        'data': group_schema.dump(group),
    })


@api.route('/group/<group_id>', methods=['DELETE'])
def delete_group(group_id):

    group = Group.query.filter(Group.id == group_id).first()

    if not group:
        return jsonify({'status': 'No such group'}), 400

    try:
        db.session.delete(group)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'status': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'status': f'Could not delete group'}), 500

    return jsonify({
        'status': 'Group deleted',
        'data': group_schema.dump(group),
    })
