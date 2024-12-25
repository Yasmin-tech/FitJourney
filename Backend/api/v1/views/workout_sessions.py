#!/usr/bin/env python3
""" API endpoints for the workout_sessions """

from . import views_bp
from models.base import db
from models.workout_session import WorkoutSession
from models.day import Day
from flask import request, jsonify, abort, url_for


@views_bp.route('/workout_sessions', methods=['GET'], strict_slashes=False)
def get_all_workout_sessions():
    """ Retrieve all the workout_sessions from the database """
    query = db.select(WorkoutSession)
    workout_sessions = db.session.execute(query).scalars().all()

    if not workout_sessions:
        return jsonify([]), 200
    # Return the workout_sessions as a json object
    return jsonify([workout_session.to_dict() for workout_session in workout_sessions]), 200


@views_bp.route('/workout_sessions/<int:workout_session_id>', methods=['GET'], strict_slashes=False)
def get_one_workout_session(workout_session_id):
    """ Retrieve a single workout_session from the database """
    workout_session = db.session.get(WorkoutSession, workout_session_id)

    if workout_session is None:
        return abort(404, description="Workout Session not found")
    # Return the workout_session as a json object
    return jsonify(workout_session.to_dict()), 200


@views_bp.route('/days/<int:day_id>/workout_sessions', methods=['GET'], strict_slashes=False)
def get_day_workout_sessions(day_id):
    """ Retrieve all the workout_sessions for a specific day """
    day = db.session.get(Day, day_id)

    if day is None:
        return abort(404, description="Day not found")
    workout_sessions = day.workout_sessions
    # Return the workout_sessions as a json object
    return jsonify([workout_session.to_dict() for workout_session in workout_sessions]), 200

@views_bp.route('/days/<int:day_id>/workout_sessions/<int:workout_session_id>', methods=['GET'], strict_slashes=False)
def get_day_workout_session(day_id, workout_session_id):
    """ Retrieve a single workout_session for a specific day """
    day = db.session.get(Day, day_id)

    # Check if the day exists
    if day is None:
        return abort(404, description="Day not found")
    
    workout_session = next((workout_session for workout_session in day.workout_sessions if workout_session.id == workout_session_id), None)
    # Return the workout_session as a json object
    if workout_session is None:
        return abort(404, description="Workout Session not found")
    
    return jsonify(workout_session.to_dict()), 200


@views_bp.route('/days/<int:day_id>/workout_sessions', methods=['POST'], strict_slashes=False)
def create_day_workout_session(day_id):
    """ Create a new workout_session for a specific day """
    day = db.session.get(Day, day_id)

    if day is None:
        return abort(404, description="Day not found")
    
    data = request.get_json()
    # Check if the request is a json object
    if not data:
        return abort(400, description="Bad Request: Not a JSON")
    
    # Check if the required fields are in the json object
    if "sets" not in data:
        return abort(400, description="Bad Request: Missing sets")
    if "reps" not in data:
        return abort(400, description="Bad Request: Missing reps")
    if "rest" not in data:
        return abort(400, description="Bad Request: Missing rest")
    
    workout_session = WorkoutSession(**data, day_id=day_id)

    # Save the workout_session to the database
    db.session.add(workout_session)
    day.workout_sessions.append(workout_session)
    db.session.commit()
    # Return the workout_session as a json object
    return jsonify(workout_session.to_dict()), 201


@views_bp.route('/days/<int:day_id>/workout_sessions/<int:workout_session_id>', methods=['PUT'], strict_slashes=False)
def update_day_workout_session(day_id, workout_session_id):
    """ Update a workout_session for a specific day """

    # Check if the day exists
    day = db.session.get(Day, day_id)
    if day is None:
        return abort(404, description="Day not found")
    
    # Check if the workout_session exists
    workout_session = next((workout_session for workout_session in day.workout_sessions if workout_session.id == workout_session_id), None)
    if workout_session is None:
        return abort(404, description="Workout Session not found")

    data = request.get_json()
    # Check if the request is a json object
    if not data:
        return abort(400, description="Bad Request: Not a JSON")

    allowed_keys = ["sets", "reps", "rest", "weight_lifted"]

    for key, value in data.items():
        if key not in allowed_keys:
            return abort(400, description=f"Bad Request: Invalid key {key}")
        setattr(workout_session, key, value)
    
    # Save the workout_session to the database
    db.session.commit()
    # Return the workout_session as a json object
    return jsonify(workout_session.to_dict()), 200


@views_bp.route('/days/<int:day_id>/workout_sessions/<int:workout_session_id>', methods=['DELETE'], strict_slashes=False)
def remove_day_workout_session(day_id, workout_session_id):
    """ Remove a workout_session for a specific day """

    # Check if the day exists
    day = db.session.get(Day, day_id)
    if day is None:
        return abort(404, description="Day not found")
    
    # Check if the workout_session exists
    workout_session = next((workout_session for workout_session in day.workout_sessions if workout_session.id == workout_session_id), None)
    if workout_session is None:
        return abort(404, description="Workout Session not found")

    # Remove the workout_session from the database
    db.session.delete(workout_session)
    db.session.commit()
    # Return an empty response
    return jsonify({"message": "Workout Session deleted"}), 200
