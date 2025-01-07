#!/usr/bin/env python3
""" Decorators for the Flask app """


from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.user import User


def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            current_user_email = get_jwt_identity()
            user = User.find_user_by_email(current_user_email)

            if not user or not any(role.name in roles for role in user.roles):
                return jsonify({"message": "Access forbidden: Insufficient permissions"}), 403

            return f(*args, **kwargs)
        return decorated_function
    return decorator
