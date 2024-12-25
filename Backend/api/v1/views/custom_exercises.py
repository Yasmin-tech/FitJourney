#!/usr/bin/env python3
""" API endpoints for the custom_exercise """


from . import views_bp
from models.base import db
from models.custom_exercise import CustomExercise
from models.user import User
from flask import request, jsonify, abort, url_for


@views_bp.route('/custom_exercises', methods=['GET'], strict_slashes=False)
def get_all_custom_exercises():
    """ Retrieve all the custom exercises from the database """
    query = db.select(CustomExercise)
    custom_exercises = db.session.execute(query).scalars().all()

    if not custom_exercises:
        return jsonify([]), 200
    # Return the custom_exercises as a list json object
    return jsonify([custom_exercise.to_dict() for custom_exercise in custom_exercises]), 200


@views_bp.route('/custom_exercises/<int:custom_exercise_id>', methods=['GET'], strict_slashes=False)
def get_one_custom_exercise(custom_exercise_id):
    """ Retrieve a single custom_exercise from the database """
    custom_exercise = db.session.get(CustomExercise, custom_exercise_id)

    if custom_exercise is None:
        return abort(404, description="Custom Exercise not found")
    # Return the exercise as a json object
    return jsonify(custom_exercise.to_dict()), 200


@views_bp.route('/users/<int:user_id>/custom_exercises', methods=['GET'], strict_slashes=False)
def get_user_custom_exercises(user_id):
    """ Retrieve all the custom exercises from a specific user """
    user = db.session.get(User, user_id)

    if user is None:
        return abort(404, description="User not found")
    # Return the custom_exercises as a list json object
    return jsonify([custom_exercise.to_dict() for custom_exercise in user.custom_exercises]), 200


@views_bp.route('/users/<int:user_id>/custom_exercises/<int:custom_exercise_id>', methods=['GET'], strict_slashes=False)
def get_user_custom_exercise(user_id, custom_exercise_id):
    """ Retrieve a single custom_exercise from a specific user """

    user = db.session.get(User, user_id)
    if user is None:
        return abort(404, description="User not found")

    custom_exercise = next((custom_exercise for custom_exercise in user.custom_exercises if custom_exercise.id == custom_exercise_id), None)

    if custom_exercise is None:
        return abort(404, description="Custom Exercise not found")
    # Return the custom_exercise as a json object
    return jsonify(custom_exercise.to_dict()), 200

@views_bp.route('/users/<int:user_id>/custom_exercises', methods=['POST'], strict_slashes=False)
def create_exercise_fot_user(user_id):
    """ Create a new exercise for a specific user """
    
    user = db.session.get(User, user_id)
    if user is None:
        return abort(404, description="User not found")

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
    query = db.select(CustomExercise).where(CustomExercise.title == data["title"])
    custom_exercise = db.session.execute(query).scalar()

    if custom_exercise:
        return abort(409, description="Conflict: Custom Exercise already exists")
    
    # Create the new exercise
    new_custom_exercise = CustomExercise(**data, user_id=user_id)
    db.session.add(new_custom_exercise)
    db.session.commit()
    # Return the new exercise as a json object
    return jsonify(new_custom_exercise.to_dict()), 201


@views_bp.route('/users/<int:user_id>/custom_exercises/<int:custom_exercise_id>', methods=['PUT'], strict_slashes=False)
def update_custom_exercise(user_id, custom_exercise_id):
    """ Update an existing exercise """
    
    # Check if the user exists
    user = db.session.get(User, user_id)
    if user is None:
        return abort(404, description="User not found")

    # Check if the exercise exists
    custom_exercise = next((custom_exercise for custom_exercise in user.custom_exercises if custom_exercise.id == custom_exercise_id), None)

    data = request.get_json()
    # Check if the request is a json object
    if not data:
        return abort(400, description="Bad Request: Not a JSON")
    
    allowed_keys = ["title", "description", "category", "muscle_group", "equipment", "video_url", "img_url"]
    
    # Update the exercise
    for key, value in data.items():
        if key not in allowed_keys:
            return abort(400, description=f"Bad Request: Invalid Key {key}")
        setattr(custom_exercise, key, value)
    db.session.commit()
    # Return the updated exercise as a json object
    return jsonify(custom_exercise.to_dict()), 200


@views_bp.route('/users/<int:user_id>/custom_exercises/<int:custom_exercise_id>', methods=['DELETE'], strict_slashes=False)
def delete_custom_exercise(user_id, custom_exercise_id):
    """ Delete the custom_exercise from the database """
    
    # Check if the user exists
    user = db.session.get(User, user_id)
    if user is None:
        return abort(404, description="User not found")

    # Check if the custom_exercise exists
    custom_exercise = next((custom_exercise for custom_exercise in user.custom_exercises if custom_exercise.id == custom_exercise_id), None)

    if custom_exercise is None:
        return abort(404, description="Custom Exercise not found")
    
    db.session.delete(custom_exercise)
    db.session.commit()
    # Return a success message
    return jsonify({"message": "Custom Exercise deleted successfully"}), 200
