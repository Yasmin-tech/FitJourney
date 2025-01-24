#!/usr/bin/env python3
""" API endpoints for the records """


from . import views_bp
from models.base import db
from models.record import Record
from models.user import User
from models.exercise import Exercise
from models.custom_exercise import CustomExercise
from flask import request, jsonify, abort, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from decorators import roles_required, user_exists


@views_bp.route("/records", methods=["GET"], strict_slashes=False)
@roles_required("Admin", "Developer")
def get_records():
    """Get all the records"""
    query = db.select(Record)
    records = db.session.execute(query).scalars().all()

    if not records:
        return jsonify([]), 200
    # Return the records as a json object
    return jsonify([record.to_dict() for record in records]), 200


@views_bp.route("/records/<int:record_id>", methods=["GET"], strict_slashes=False)
@roles_required("Admin", "Developer")
def get_one_record(record_id):
    """Get a single record"""
    record = db.session.get(Record, record_id)

    if record is None:
        return abort(404, description="Record not found")
    # Return the record as a json object
    return jsonify(record.to_dict()), 200


@views_bp.route("/users/<int:user_id>/records", methods=["GET"], strict_slashes=False)
@jwt_required()
@user_exists
def get_user_records(user_id):
    """Get all the records from a specific user"""

    user = db.session.get(User, user_id)
    if user is None:
        return abort(404, description="User not found")

    # Check the log in user credentials
    log_in_user_email = get_jwt_identity()
    log_in_user = db.session.query(User).filter_by(email=log_in_user_email).first()
    roles = [role.name for role in log_in_user.roles]
    if (
        user.email != log_in_user_email
        and "Admin" not in roles
        and "Developer" not in roles
    ):
        return abort(
            403, description="Forbidden: User does not have access to this resource"
        )

    # Return the records as a json object
    return jsonify([record.to_dict() for record in user.records]), 200


@views_bp.route(
    "/users/<int:user_id>/records/<int:record_id>",
    methods=["GET"],
    strict_slashes=False,
)
@jwt_required()
@user_exists
def get_one_record_from_user(user_id, record_id):
    """Get a single record from a specific user"""

    user = db.session.get(User, user_id)
    if user is None:
        return abort(404, description="User not found")

    # Check the log in user credentials
    log_in_user_email = get_jwt_identity()
    log_in_user = db.session.query(User).filter_by(email=log_in_user_email).first()
    roles = [role.name for role in log_in_user.roles]
    if (
        user.email != log_in_user_email
        and "Admin" not in roles
        and "Developer" not in roles
    ):
        return abort(
            403, description="Forbidden: User does not have access to this resource"
        )

    # Check if the record exists
    record = next((record for record in user.records if record.id == record_id), None)

    if record is None:
        return abort(404, description="Record not found")
    # Return the record as a json object
    return jsonify(record.to_dict()), 200


@views_bp.route("/users/<int:user_id>/records", methods=["POST"], strict_slashes=False)
@jwt_required()
@user_exists
def create_record_for_user(user_id):
    """Create a new record for a specific user"""

    # Check if the user exists
    user = db.session.get(User, user_id)
    if user is None:
        return abort(404, description="User not found")

    # Check the log in user credentials
    log_in_user_email = get_jwt_identity()
    log_in_user = db.session.query(User).filter_by(email=log_in_user_email).first()
    roles = [role.name for role in log_in_user.roles]
    if (
        user.email != log_in_user_email
        and "Admin" not in roles
        and "Developer" not in roles
    ):
        return abort(
            403, description="Forbidden: User does not have access to this resource"
        )

    # Check if the request is a json object
    data = request.get_json()
    if not data:
        return abort(400, description="Bad Request: Not a JSON")

    # Check if the required fields are in the json object
    if "difficulty" not in data:
        return abort(400, description="Bad Request: Missing difficulty")
    if "sets" not in data:
        return abort(400, description="Bad Request: Missing sets")
    if "reps" not in data:
        return abort(400, description="Bad Request: Missing reps")
    if "rest" not in data:
        return abort(400, description="Bad Request: Missing rest")
    if "user_weight" not in data:
        return abort(400, description="Bad Request: Missing user_weight")
    if "location" not in data:
        return abort(400, description="Bad Request: Missing location")

    # If the json object has exercise_id, check if the exercise exists
    if "exercise_id" in data:
        exercise = db.session.get(Exercise, data["exercise_id"])
        if exercise is None:
            return abort(404, description="Exercise not found")

    # If the json object has custom_exercise_id, check if the exercise exists
    if "custom_exercise_id" in data:
        custom_exercise = db.session.get(CustomExercise, data["custom_exercise_id"])
        if custom_exercise is None:
            return abort(404, description=" Custom exercise not found")

    # Create the new record
    new_record = Record(**data, user_id=user_id)

    # Save the record to the database
    db.session.add(new_record)
    db.session.commit()
    user.records.append(new_record)

    # Return the record as a json object
    return jsonify(new_record.to_dict()), 201


@views_bp.route(
    "users/<int:user_id>/records/<int:record_id>", methods=["PUT"], strict_slashes=False
)
@jwt_required()
@user_exists
def update_record(user_id, record_id):
    """Update an existing record"""

    # Check if the user exists
    user = db.session.get(User, user_id)
    if user is None:
        return abort(404, description="User not found")

    # Check the log in user credentials
    log_in_user_email = get_jwt_identity()
    log_in_user = db.session.query(User).filter_by(email=log_in_user_email).first()
    roles = [role.name for role in log_in_user.roles]
    if (
        user.email != log_in_user_email
        and "Admin" not in roles
        and "Developer" not in roles
    ):
        return abort(
            403, description="Forbidden: User does not have access to this resource"
        )

    # Check if the record exists
    record = next((record for record in user.records if record.id == record_id), None)
    if record is None:
        return abort(404, description="Record not found")

    # Check if the request is a json object
    data = request.get_json()
    if not data:
        return abort(400, description="Bad Request: Not a JSON")

    allowed_keys = [
        "exercise_id",
        "custom_exercise_id",
        "difficulty",
        "sets",
        "reps",
        "rest",
        "weight_lifted",
        "user_weight",
        "location",
        "notes",
    ]
    # Update the record
    for key, value in data.items():
        if key not in allowed_keys:
            return abort(400, description=f"Bad Request: Invalid key {key}")
        if key == "exercise_id":
            exercise = db.session.get(Exercise, value)
            if exercise is None:
                return abort(404, description="Exercise not found")
        if key == "custom_exercise_id":
            custom_exercise = db.session.get(CustomExercise, value)
            if custom_exercise is None:
                return abort(404, description="Custom Exercise not found")

        setattr(record, key, value)

    # Save the record to the database
    db.session.commit()

    # Return the record as a json object
    return jsonify(record.to_dict()), 200


@views_bp.route(
    "users/<int:user_id>/records/<int:record_id>",
    methods=["DELETE"],
    strict_slashes=False,
)
@jwt_required()
@user_exists
def remove_record(user_id, record_id):
    """Delete a record from the database of a specific user"""

    # Check if the user exists
    user = db.session.get(User, user_id)
    if user is None:
        return abort(404, description="User not found")

    # Check the log in user credentials
    log_in_user_email = get_jwt_identity()
    log_in_user = db.session.query(User).filter_by(email=log_in_user_email).first()
    roles = [role.name for role in log_in_user.roles]
    if (
        user.email != log_in_user_email
        and "Admin" not in roles
        and "Developer" not in roles
    ):
        return abort(
            403, description="Forbidden: User does not have access to this resource"
        )

    # Check if the record exists
    record = next((record for record in user.records if record.id == record_id), None)
    if not record:
        return abort(404, description="Record not found")

    # Remove the record from the database
    db.session.delete(record)
    db.session.commit()

    return jsonify({"message": "Record deleted successfully"}), 200
