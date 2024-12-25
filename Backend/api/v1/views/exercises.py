#!/usr/bin/env python3
""" API endpoints for the exercises """


from . import views_bp
from models.base import db
from models.exercise import Exercise
from flask import request, jsonify, abort, url_for


@views_bp.route('/exercises', methods=['GET'], strict_slashes=False)
def get_all_exercises():
    """ Retrieve all the exercises from the database """
    query = db.select(Exercise)
    exercises = db.session.execute(query).scalars().all()

    if not exercises:
        return jsonify([]), 200
    # Return the exercises as a json object
    return jsonify([exercise.to_dict() for exercise in exercises]), 200


@views_bp.route('/exercises/<int:exercise_id>', methods=['GET'], strict_slashes=False)
def get_one_exercise(exercise_id):
    """ Retrieve a single exercise from the database """
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return abort(404, description="Exercise not found")
    # Return the exercise as a json object
    return jsonify(exercise.to_dict()), 200


@views_bp.route('/exercises', methods=['POST'], strict_slashes=False)
def create_exercise():
    """ Create a new exercise """
    
    data = request.get_json()
    # Check if the request is a json object
    if not data:
        return abort(400, description="Bad Request: Not a JSON")
    
    # Check if the required fields are in the json object
    if "title" not in data:
        return abort(400, description="Bad Request: Missing title")
    if "category" not in data:
        return abort(400, description="Bad Request: Missing category")
    if "muscle_group" not in data:
        return abort(400, description="Bad Request: Missing muscle_group")
    
    # Check if the exercise already exists
    query = db.select(Exercise).where(Exercise.title == data["title"])
    exercise = db.session.execute(query).scalar()

    if exercise:
        return abort(409, description="Conflict: Exercise already exists")
    
    # Create the new exercise
    exercise = Exercise(**data)
    db.session.add(exercise)
    db.session.commit()
    # Return the new exercise as a json object
    return jsonify(exercise.to_dict()), 201


@views_bp.route('/exercises/<int:exercise_id>', methods=['PUT'], strict_slashes=False)
def update_exercise(exercise_id):
    """ Update an existing exercise """
    
    # Check if the exercise exists
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return abort(404, description="Exercise not found")

    data = request.get_json()
    # Check if the request is a json object
    if not data:
        return abort(400, description="Bad Request: Not a JSON")
    
    allowed_keys = ["title", "description", "category", "muscle_group", "equipment", "video_url", "img_url"]
    
    # Update the exercise
    for key, value in data.items():
        if key not in allowed_keys:
            return abort(400, description=f"Bad Request: Invalid Key {key}")
        setattr(exercise, key, value)
    db.session.commit()
    # Return the updated exercise as a json object
    return jsonify(exercise.to_dict()), 200


@views_bp.route('/exercises/<int:exercise_id>', methods=['DELETE'], strict_slashes=False)
def delete_exercise(exercise_id):
    """ Delete an exercise from the database """
    
    # Check if the exercise exists
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return abort(404, description="Exercise not found")
    
    db.session.delete(exercise)
    db.session.commit()
    # Return a success message
    return jsonify({"message": "Exercise deleted successfully"}), 200
