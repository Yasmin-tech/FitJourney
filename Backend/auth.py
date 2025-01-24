#!/usr/bin/env python3
"""
    Manage user authentication and authorization
"""


from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from models.user import User
from models.role import Role
from decorators import roles_required
import requests


auth_bp = Blueprint("auth_pb", __name__, url_prefix="/auth")


def validate_signup_data(data):
    """Helper function to validate signup data"""
    required_fields = ["first_name", "last_name", "email", "password"]
    return all(field in data for field in required_fields)


@auth_bp.route("/signup", methods=["POST"], strict_slashes=False)
def signup_user():
    """Sign up the user"""
    data = request.get_json()
    if not data or not validate_signup_data(data):
        return jsonify({"message": "Missing fields in request"}), 400

    response = requests.post("http://localhost:5000/api/v1/users", json=data)
    if response.status_code == 201:
        return (
            jsonify(
                {"message": "User created successfully", "new_user": response.json()}
            ),
            201,
        )
    if response.status_code == 409:
        return jsonify({"message": "User already exists"}), 409
    return (
        jsonify({"error": "Something went wrong", "details": response.json()}),
        response.status_code,
    )


def validate_login_data(data):
    """Helper function to validate login data"""
    return "email" in data and "password" in data


@auth_bp.route("/login", methods=["POST"], strict_slashes=False)
def log_in():
    """Log in the user"""
    data = request.get_json()
    if not data or not validate_login_data(data):
        return jsonify({"message": "Missing fields in request"}), 400

    user = User.find_user_by_email(data["email"])
    if not user:
        return jsonify({"message": "User does not exist"}), 404

    if not user.check_password(data["password"]):
        return jsonify({"message": "Unauthorized, Invalid password"}), 401

    access_token = create_access_token(identity=user.email)
    refresh_token = create_refresh_token(identity=user.email)
    return (
        jsonify(
            {
                "message": "Logged in successfully",
                "user": user.to_dict(),
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        ),
        200,
    )


@auth_bp.route("/admin/login", methods=["POST"], strict_slashes=False)
def admin_login():
    """Log in the admin user"""
    data = request.get_json()
    if not data or not validate_login_data(data):
        return jsonify({"message": "Missing fields in request"}), 400

    user = User.find_user_by_email(data["email"])
    if not user:
        return jsonify({"message": "User does not exist"}), 404

    if not user.check_password(data["password"]):
        return jsonify({"message": "Unauthorized, Invalid password"}), 401

    if not user.is_admin():
        return jsonify({"message": "Unauthorized, Insufficient permissions"}), 403

    access_token = create_access_token(identity=user.email)
    refresh_token = create_refresh_token(identity=user.email)
    return (
        jsonify(
            {
                "message": "Admin logged in successfully",
                "user": user.to_dict(),
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        ),
        200,
    )


@auth_bp.route(
    "/admin/create_users_roles/<int:user_id>/<role_name>",
    methods=["POST"],
    strict_slashes=False,
)
@roles_required("Admin")
def create_users_roles(user_id, role_name):
    """Create a new role if it does not exist and assign it to a user"""

    # Obtain the JWT token from the current request
    current_token = request.headers.get("Authorization", None).split(" ")[1]
    headers = {
        "Authorization": f"Bearer {current_token}",
        "Content-Type": "application/json",
    }

    user_response = requests.get(
        f"http://localhost:5000/api/v1/users/{user_id}", headers=headers
    )
    if user_response.status_code == 404:
        return jsonify({"message": "User not found"}), 404

    role_response = requests.post(
        "http://localhost:5000/api/v1/roles",
        json={"role_name": role_name},
        headers=headers,
    )
    if role_response.status_code in [201, 409]:
        assign_role_response = requests.post(
            f"http://localhost:5000/api/v1/users/{user_id}/roles/{role_name}",
            headers=headers,
        )
        if assign_role_response.status_code == 201:
            return (
                jsonify(
                    {"message": f"Role {role_name} assigned successfully to this user"}
                ),
                201,
            )
        return (
            jsonify(
                {
                    "error": f"Something went wrong when assigning role {role_name} to user",
                    "details": assign_role_response.json(),
                }
            ),
            assign_role_response.status_code,
        )
    return (
        jsonify(
            {
                "error": f"Something went wrong when creating a role {role_name}",
                "details": role_response.json(),
            }
        ),
        role_response.status_code,
    )


@auth_bp.route("/refresh", methods=["POST"], strict_slashes=False)
@jwt_required(refresh=True)
def refresh():
    """Refresh the access token"""
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token), 200
