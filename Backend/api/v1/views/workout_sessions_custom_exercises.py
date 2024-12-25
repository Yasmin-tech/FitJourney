#!/usr/bin/env python3
""" API endpoints for the many-to-many relationship between
    workout_sessions and custom_exercises """

from . import views_bp
from models.base import db
from models.workout_session import WorkoutSession
from models.workout_session import workout_sessions_custom_exercises
from models.custom_exercise import CustomExercise
from flask import request, jsonify, abort


@views_bp.route('/workout_sessions/<int:workout_session_id>/custom_exercises', methods=['GET'], strict_slashes=False)
def get_workout_session_custom_exercises(workout_session_id):
    """ Retrieve all the custom exercises for a specific workout session """
    workout_session = db.session.get(WorkoutSession, workout_session_id)

    if workout_session is None:
        return abort(404, description="Workout Session not found")
    custom_exercises = workout_session.custom_exercises
    # Return the custom exercises as a json object
    return jsonify([custom_exercise.to_dict() for custom_exercise in custom_exercises]), 200


@views_bp.route('/workout_sessions/<int:workout_session_id>/custom_exercises/<int:custom_exercise_id>', methods=['GET'], strict_slashes=False)
def get_one_workout_session_custom_exercise(workout_session_id, custom_exercise_id):
    """ Retrieve a single custom exercise for a specific workout session """
    workout_session = db.session.get(WorkoutSession, workout_session_id)

    if workout_session is None:
        return abort(404, description="Workout Session not found")

    custom_exercise = next((custom_exercise for custom_exercise in workout_session.custom_exercises if custom_exercise.id == custom_exercise_id), None)
    # Return the custom exercise as a json object
    if custom_exercise is None:
        return abort(404, description="Custom Exercise not found in this workout session")

    return jsonify(custom_exercise.to_dict()), 200


@views_bp.route(
    '/workout_sessions/<int:workout_session_id>/custom_exercises/<int:custom_exercise_id>/workout_sessions_custom_exercises',
    methods=['POST'], strict_slashes=False)
def link_workout_sessions_to_custom_exercises(workout_session_id, custom_exercise_id):
    """ Link a workout session to a custom exercise """

    workout_session = db.session.get(WorkoutSession, workout_session_id)
    if workout_session is None:
        return abort(404, description="Workout Session not found")

    custom_exercise = db.session.get(CustomExercise, custom_exercise_id)
    if custom_exercise is None:
        return abort(404, description="Custom Exercise not found")

    # insert and workout_session and custom_exercise into the association table
    if custom_exercise not in workout_session.custom_exercises:
        workout_session.custom_exercises.append(custom_exercise)

    db.session.commit()
    # Return the custom exercise as a json object
    return jsonify({"workout_session_id": workout_session_id, "custom_exercise_id": custom_exercise_id}), 201


@views_bp.route('/workout_sessions/<int:workout_session_id>/custom_exercises', methods=['PUT'], strict_slashes=False)
def update_workout_session_custom_exercises(workout_session_id):
    """ Update the custom exercises for a specific workout session 
        with a new list of custom exercises """
    workout_session = db.session.get(WorkoutSession, workout_session_id)

    if workout_session is None:
        return abort(404, description="Workout Session not found")

    data = request.get_json()
    if not data or "custom_exercises" not in data:
        return abort(400, description="Bad Request: Missing custom exercise data")

    # clear the custom_exercises list
    workout_session.custom_exercises = []

    for custom_exercise_id in data["custom_exercises"]:
        custom_exercise = db.session.get(CustomExercise, custom_exercise_id)
        if custom_exercise is None:
            return abort(404, description="Custom Exercise not found")
        workout_session.custom_exercises.append(custom_exercise)
    
    db.session.commit()
    # Return the custom exercises as a json object
    return jsonify([custom_exercise.to_dict() for custom_exercise in workout_sessions_exercises]), 200


@views_bp.route('/workout_sessions/<int:workout_session_id>/custom_exercises/<int:custom_exercise_id>', methods=['DELETE'], strict_slashes=False)
def unlink_workout_sessions_to_custom_exercises(workout_session_id, custom_exercise_id):
    """ Unlink a workout session from a custom exercise """

    workout_session = db.session.get(WorkoutSession, workout_session_id)
    if workout_session is None:
        return abort(404, description="Workout Session not found")

    custom_exercise = db.session.get(CustomExercise, custom_exercise_id)
    if custom_exercise is None:
        return abort(404, description="Custom Exercise not found")

    # Remove the association
    if custom_exercise in workout_session.custom_exercises:
        workout_session.custom_exercises.remove(custom_exercise)

    db.session.commit()
    # Return the custom exercise as a json object
    return jsonify({"message": "The custom_exercise is deleted from this workout_session successfully"}), 200
