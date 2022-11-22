from functools import wraps

from app.accounts.role import Role
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, current_user


def grant_access(roles=None, match=False, user_id_param_name='user_id'):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):

            verify_jwt_in_request()

            if match and user_id_param_name and kwargs.get(user_id_param_name) and \
                    kwargs.get(user_id_param_name) != current_user.id and not current_user.has_role([Role.admin]):
                return jsonify(msg="No access!"), 403

            if not roles or current_user.has_role(roles):
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="No access!"), 403

        return decorator

    return wrapper
