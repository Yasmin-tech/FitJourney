#!/usr/bin/env python3
""" API endpoints for the records """


from . import views_bp
from models.base import db
from models.record import Record
from models.user import User
from models.exercise import Exercise
from models.custom_exercise import CustomExercise
from flask import request, jsonify, abort, url_for
from flask_jwt_extended import jwt_required
from decorators import roles_required


@views_bp.route('/records', methods=['GET'], strict_slashes=False)
@roles_required('Admin', 'Developer')
def get_records():
    """ Get all the records """
    query = db.select(Record)
    records = db.session.execute(query).scalars().all()

    if not records:
        return jsonify([]), 200
    # Return the records as a json object
    return jsonify([record.to_dict() for record in records]), 200


@views_bp.route('/records/<int:record_id>', methods=['GET'], strict_slashes=False)
@roles_required('Admin', 'Developer')
def get_one_record(record_id):
    """ Get a single record """
    record = db.session.get(Record, record_id)

    if record is None:
        return abort(404, description="Record not found")
    # Return the record as a json object
    return jsonify(record.to_dict()), 200


@views_bp.route('/users/<int:user_id>/records', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_user_records(user_id):
    """ Get all the records from a specific user """

    user = db.session.get(User, user_id)
    if user is None:
        return abort(404, description="User not found")
    # Return the records as a json object
    return jsonify([record.to_dict() for record in user.records]), 200


@views_bp.route('/users/<int:user_id>/records/<int:record_id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_one_record_from_user(user_id, record_id):
    """ Get a single record from a specific user """

    user = db.session.get(User, user_id)
    if user is None:
        return abort(404, description="User not found")

    # Check if the record exists
    record = next((record for record in user.records if record.id == record_id), None)

    if record is None:
        return abort(404, description="Record not found")
    # Return the record as a json object
    return jsonify(record.to_dict()), 200


@views_bp.route('/users/<int:user_id>/records', methods=['POST'], strict_slashes=False)
@jwt_required()
def create_record_for_user(user_id):
    """ Create a new record for a specific user """

    # Check if the user exists
    user = db.session.get(User, user_id)
    if user is None:
        return abort(404, description="User not found")
    
    # Check if the request is a json object
    data = request.get_json()
    if not data:
        return abort(400, description="Bad Request: Not a JSON")
    
    # Check if the required fields are in the json object
    if "exercise_id" not in data:
        return abort(400, description="Bad Request: Missing exercise_id")
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
    
    # Create the new record
    try:
        new_record = Record(**data, user_id=user_id)
    except TypeError:
        return abort(400, description="Bad Request: Invalid data type")
    
    new_record.exercise_id = data["exercise_id"]

    # Save the record to the database
    db.session.add(new_record)
    db.session.commit()
    user.records.append(new_record)

    # Return the record as a json object
    return jsonify(new_record.to_dict()), 201


@views_bp.route('users/<int:user_id>/records/<int:record_id>', methods=['PUT'], strict_slashes=False)
@jwt_required()
def update_record(user_id, record_id):
    """ Update an existing record """

    # Check if the user exists
    user = db.session.get(User, user_id)
    if user is None:
        return abort(404, description="User not found")

    # Check if the record exists
    record = next((record for record in user.records if record.id == record_id), None)
    if record is None:
        return abort(404, description="Record not found")

    # Check if the request is a json object
    data = request.get_json()
    if not data:
        return abort(400, description="Bad Request: Not a JSON")
    
    allowed_keys = ["exercise_id", "custom_exercise_id","difficulty", "sets", "reps", "rest", "weight_lifted", "user_weight", "location", "notes"]
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


@views_bp.route('users/<int:user_id>/records/<int:record_id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def remove_record(user_id, record_id):
    """ Delete a record from the database of a specific user """

    # Check if the user exists
    user = db.session.get(User, user_id)
    if user is None:
        return abort(404, description="User not found")
    
    # Check if the record exists
    record = next((record for record in user.records if record.id == record_id), None)
    if not record:
        return abort(404, description="Record not found")
    
    # Remove the record from the database
    db.session.delete(record)
    db.session.commit()

    return jsonify({"message": "Record deleted successfully"}), 200
