#!/usr/bin/env python3
"""
    manage user authentication
    """


from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from models.user import User
import requests
from flask_jwt_extended import jwt_required, get_jwt_identity
from decorators import roles_required

auth_bp = Blueprint('auth_pb', __name__, url_prefix='/auth')


@auth_bp.route('/signup', methods=['POST'], strict_slashes=False)
def signup_user():
    """ Sign up the user """
    # Get the user details from json data

    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')

    # Check for missing fields
    if not all([first_name, last_name, email, password]):
        return jsonify({"message": "Missing fields in request"}), 400

    # Send a POST request to the API to sign up the user
    response = requests.post('http://localhost:5001/api/v1/users', json={
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password
    })
    if response.status_code == 201:
        # If the user was created successfully, return the user details
        return jsonify({"message": "User created successfully",
                         "new_user": response.json()}), 201
    if response.status_code == 409:
        return jsonify({"message": "User already exists"}), 400
    return jsonify(response.json()), 400


@auth_bp.route('/login', methods=['POST'], strict_slashes=False)
def log_in():
    """ Log in the user """
    # Get the user details from json data
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Check for missing fields
    if not all([email, password]):
        return jsonify({"message": "Missing fields in request"}), 400

    # check if the user if the user exists
    user = User.find_user_by_email(email)
    if not user:
        return jsonify({"message": "User does not exist"}), 404
    
    # Check if the password is correct
    if not user.check_password(password):
        return jsonify({"message": "Unauthorized, Invalid password"}), 401

    # Generate a JWT token
    access_token = create_access_token(identity=user.email)
    refresh_token = create_refresh_token(identity=user.email)

    return jsonify({"message": "Logged in successfully",
                    "user": user.to_dict(),
                    "access_token": access_token,
                    "refresh_token": refresh_token}), 200


@auth_bp.route('/admin/login', methods=['POST'], strict_slashes=False)
def admin_login():
    """ Log in the admin user """
    # Get the user details from json data
    data = request.get_json()

    if not data:
        return jsonify({"message": "Bad Request: Not a JSON"}), 400

    email = data.get('email')
    password = data.get('password')

    # Check for missing fields
    if not all([email, password]):
        return jsonify({"message": "Missing fields in request"}), 400

    # check if the user if the user exists
    user = User.find_user_by_email(email)
    if not user:
        return jsonify({"message": "User does not exist"}), 404

    # Check if the password is correct
    if not user.check_password(password):
        return jsonify({"message": "Unauthorized, Invalid password"}), 401

    # Check if the user is an admin
    if not user.is_admin():
        return jsonify({"message": "Unauthorized, Insufficient permissions"}), 401

    # Generate a JWT token
    access_token = create_access_token(identity=user.email)
    refresh_token = create_refresh_token(identity=user.email)

    return jsonify({"message": "Logged in successfully",
                    "user": user.to_dict(),
                    "access_token": access_token,
                    "refresh_token": refresh_token}), 200


@auth_bp.route('/admin/create_users_roles/<int:user_id>/<role_name>', methods=['POST'], strict_slashes=False)
@roles_required('Admin')
def create_users_roles(user_id, role_name):
    """ Assign a role to a user """

    #Get the user object
    user = requests.get(f'http://localhost:5001/api/v1/users/{str(user_id)}')
    if user.status_code == 404:
        return jsonify({"message": "User not found"}), 404
    
    # Create the role
    role = requests.post('http://localhost:5001/api/v1/roles', json={"role_name": role_name})
    if role.status_code == 201 or role.status_code == 409:
        # Assign the role to the user
        response = requests.post(f'http://localhost:5001/api/v1/users/{str(user_id)}/roles/{role_name}', json={
            "email": user.json().get('email'),
            "role_name": role_name
        })
        if response.status_code == 201:
            return jsonify({"message": f"Role {role_name} assigned successfully to this user",
                            "user": user.json()}), 201
        return jsonify(response.json()), 500
    return jsonify(role.json()), 500


@auth_bp.route('/refresh', methods=['POST'], strict_slashes=False)
@jwt_required(refresh=True)
def refresh():
    """ Refresh the access token """
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token)
