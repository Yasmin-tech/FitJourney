#!/usr/bin/env python3
"""
    Manage the CRUD operations for roles
    """


from . import views_bp
from flask import request, jsonify, abort
from models.base import db
from models.role import Role
from models.user import User
from flask_jwt_extended import jwt_required
from decorators import roles_required
from flask_jwt_extended import jwt_required


# Endpoint to get all roles
@views_bp.route("/roles", methods=["GET"], strict_slashes=False)
@roles_required("Admin", "Developer")
def get_roles():
    """Get all the roles"""
    query = db.select(Role)
    roles = db.session.execute(query).scalars().all()

    if not roles:
        return jsonify([]), 200
    return jsonify([role.to_dict() for role in roles]), 200


# Endpoint to get a single role by its ID
@views_bp.route("/roles/<int:role_id>", methods=["GET"], strict_slashes=False)
@roles_required("Admin", "Developer")
def get_role(role_id):
    """Get a role by its id"""
    role = db.session.get(Role, role_id)
    if not role:
        return jsonify({"error": "Role not found"}), 404
    return jsonify(role.to_dict()), 200


# Endpoint to get all users of a specific role
@views_bp.route("/roles/<int:role_id>/users", methods=["GET"], strict_slashes=False)
@roles_required("Admin", "Developer")
def get_users_by_role(role_id):
    """Get all users of a specific role"""
    role = db.session.get(Role, role_id)
    if not role:
        return jsonify({"message": "Role not found"}), 404

    users = [user.to_dict() for user in role.users]
    return jsonify(users), 200


# Endpoint to create a new role
@views_bp.route("/roles", methods=["POST"], strict_slashes=False)
@roles_required("Admin")
def add_role():
    data = request.get_json()
    if not data or "role_name" not in data:
        return abort(400, description="Bad Request: Missing role name")

    role_name = data["role_name"]
    # Check if the role already exists
    existing_role = Role.find_role_by_name(role_name)
    if existing_role:
        return jsonify({"message": "Role already exists"}), 409

    new_role = Role(name=role_name)
    db.session.add(new_role)
    db.session.commit()
    return jsonify(new_role.to_dict()), 201


# Endpoint to update a role by its ID
@views_bp.route("/roles/<int:role_id>", methods=["PUT"], strict_slashes=False)
@roles_required("Admin")
def update_role(role_id):
    data = request.get_json()
    if not data or "role_name" not in data:
        return abort(400, description="Bad Request: Missing role name")

    role = db.session.get(Role, role_id)
    if not role:
        return jsonify({"message": "Role not found"}), 404

    # Check if the role already exists
    existing_role = Role.find_role_by_name(data["role_name"])
    if existing_role:
        return jsonify({"message": "Role already exists"}), 409
    role.name = data["role_name"]
    db.session.commit()
    return jsonify(role.to_dict()), 200


# Endpoint to delete a role by its ID
@views_bp.route("/roles/<int:role_id>", methods=["DELETE"], strict_slashes=False)
@roles_required("Admin")
def delete_role(role_id):
    role = db.session.get(Role, role_id)
    if not role:
        return jsonify({"message": "Role not found"}), 404

    db.session.delete(role)
    db.session.commit()
    return jsonify({"message": "Role deleted successfully"}), 200
