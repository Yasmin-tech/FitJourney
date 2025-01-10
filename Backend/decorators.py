from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User


def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get('Authorization', None)
            if not auth_header:
                return jsonify({"message": "Authorization header is missing."}), 401

            current_user_email = get_jwt_identity()
            user = User.find_user_by_email(current_user_email)

            if not user:
                return jsonify({"msg": "Invalid authentication credentials."}), 401

            if not any(role.name in roles for role in user.roles):
                return jsonify({"message": f"Access forbidden: User does not have the required roles {roles}."}), 403

            return f(*args, **kwargs)
        return decorated_function
    return decorator
