#!/usr/bin/env python3
""" API endpoints for the many-to-many relationship between
    workout_sessions and exercises """

from . import views_bp
from models.base import db
from models.workout_session import WorkoutSession
from models.workout_session import workout_sessions_exercises
from models.exercise import Exercise
from flask import request, jsonify, abort
from flask_jwt_extended import jwt_required


@views_bp.route('/workout_sessions/<int:workout_session_id>/exercises', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_workout_session_exercises(workout_session_id):
    """ Retrieve all the exercises for a specific workout session """
    workout_session = db.session.get(WorkoutSession, workout_session_id)

    if workout_session is None:
        return abort(404, description="Workout Session not found")
    exercises = workout_session.exercises
    # Return the exercises as a json object
    return jsonify([exercise.to_dict() for exercise in exercises]), 200


@views_bp.route('/workout_sessions/<int:workout_session_id>/exercises/<int:exercise_id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_one_workout_session_exercise(workout_session_id, exercise_id):
    """ Retrieve a single exercise for a specific workout session """
    workout_session = db.session.get(WorkoutSession, workout_session_id)

    # Check if the workout_session exists
    if workout_session is None:
        return abort(404, description="Workout Session not found")
    
    exercise = next((exercise for exercise in workout_session.exercises if exercise.id == exercise_id), None)
    # Return the exercise as a json object
    if exercise is None:
        return abort(404, description="Exercise not found in this workout session")
    
    return jsonify(exercise.to_dict()), 200


@views_bp.route('/workout_sessions/<int:workout_session_id>/exercises/<int:exercise_id>/workout_sessions_exercises', methods=['POST'], strict_slashes=False)
@jwt_required()
def link_workout_sessions_to_exercises(workout_session_id, exercise_id):
    """ Link a workout session to an exercise """

    workout_session = db.session.get(WorkoutSession, workout_session_id)
    if workout_session is None:
        return abort(404, description="Workout Session not found")

    exercise = db.session.get(Exercise, exercise_id)
    if exercise is None:
        return abort(404, description="Exercise not found")

    # insert and workout_session and exercise into the association table
    if exercise not in workout_session.exercises:
        workout_session.exercises.append(exercise)

    db.session.commit()
    # Return the exercise as a json object
    return jsonify({"workout_session_id": workout_session_id, "exercise_id": exercise_id}), 201


@views_bp.route('/workout_sessions/<int:workout_session_id>/exercises', methods=['PUT'], strict_slashes=False)
@jwt_required()
def update_workout_session_exercises(workout_session_id):
    """ Update the exercises for a specific workout session 
        with a new list of exercises """
    workout_session = db.session.get(WorkoutSession, workout_session_id)

    if workout_session is None:
        return abort(404, description="Workout Session not found")

    data = request.get_json()
    if not data or "exercises" not in data:
        return abort(400, description="Bad Request: Missing exercise data")

    # Clear current associations
    workout_session.exercises = []

    # Add new associations
    for exercise_id in data["exercises"]:
        exercise = db.session.get(Exercise, exercise_id)
        if exercise:
            workout_session.exercises.append(exercise)

    db.session.commit()
    return jsonify([exercise.to_dict() for exercise in workout_session.exercises]), 200


@views_bp.route('/workout_sessions/<int:workout_session_id>/exercises/<int:exercise_id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def unlink_workout_sessions_to_exercises(workout_session_id, exercise_id):
    """ Unlink a workout session from an exercise """

    workout_session = db.session.get(WorkoutSession, workout_session_id)
    if workout_session is None:
        return abort(404, description="Workout Session not found")

    exercise = db.session.get(Exercise, exercise_id)
    if exercise is None:
        return abort(404, description="Exercise not found")

    # Remove the association
    if exercise in workout_session.exercises:
        workout_session.exercises.remove(exercise)

    db.session.commit()
    return jsonify({"message": "The exercise is deleted from this workout_session successfully"}), 200
