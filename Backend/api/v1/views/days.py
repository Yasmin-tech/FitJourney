#!/usr/bin/env python3
""" API endpoints for the days """


from . import views_bp
from models.base import db
from models.day import Day
from models.plan import Plan
from flask import request, jsonify, abort


@views_bp.route('/days', methods=['GET'], strict_slashes=False)
def get_all_days():
    """ Retrieve all the days from the database """
    query = db.select(Day)
    days = db.session.execute(query).scalars().all()

    if not days:
        return jsonify([]), 200
    # Return the days as a json object
    return jsonify([day.to_dict() for day in days])


@views_bp.route('/days/<int:day_id>', methods=['GET'], strict_slashes=False)
def get_one_day(day_id):
    """ Retrieve a single day from the database """
    day = db.session.get(Day, day_id)

    if day is None:
        return abort(404, description="Day not found")
    # Return the day as a json object
    return jsonify(day.to_dict()), 200


@views_bp.route('/plans/<int:plan_id>/days', methods=['GET'], strict_slashes=False)
def get_all_days_for_plan(plan_id):
    """ Retrieve all the days for a specific plan """
    plan = db.session.get(Plan, plan_id)

    if not plan:
        return abort(404, description="Plan not found")

    # Access the days attribute of the plan object
    days = plan.days
    if not days:
        return jsonify([]), 200

    # Return the days as a json object
    return jsonify([day.to_dict() for day in days])


@views_bp.route('/plans/<int:plan_id>/days/<int:day_id>', methods=['GET'], strict_slashes=False)
def get_one_day_for_plan(plan_id, day_id):
    """ Retrieve a single day for a specific plan """
    plan = db.session.get(Plan, plan_id)

    if not plan:
        return abort(404, description="Plan not found")

    # Access the days attribute of the plan object
    # This generator expression will return the day object if the day_id matches
    day = next((day for day in plan.days if day.id == day_id), None)

    if day is None:
        return abort(404, description="Day not found")
    # Return the day as a json object
    return jsonify(day.to_dict()), 200


@views_bp.route('/plans/<int:plan_id>/days', methods=['POST'], strict_slashes=False)
def create_one_day_for_plan(plan_id):
    """ Create a new day for a specific plan """

    plan = db.session.get(Plan, plan_id)

    if not plan:
        return abort(404, description="Plan not found")


    data = request.get_json()
    # Check if the request is a json object
    if not data:
        return abort(400, description="Bad Request: Not a JSON")

    # Check if the required fields are in the json object
    if "title" not in data:
        return abort(400, description="Bad Request: Missing title")

    # Create a new day
    new_day = Day(**data, plan_id=plan_id)

    # Save the day to the database
    db.session.add(new_day)
    db.session.commit()
    plan.days.append(new_day)

    # Return the day as a json object
    return jsonify(new_day.to_dict()), 201


@views_bp.route('/plans/<int:plan_id>/days/<int:day_id>', methods=['PUT'], strict_slashes=False)
def update_day_for_plan(plan_id, day_id):
    """ Update a single day for a specific plan """

    plan = db.session.get(Plan, plan_id)

    if not plan:
        return abort(404, description="Plan not found")

    day = db.session.get(Day, day_id)

    if not day:
        return abort(404, description="Day not found")

    data = request.get_json()
    # Check if the request is a json object
    if not data:
        return abort(400, description="Bad Request: Not a JSON")

    allowed_keys = ["title", "session_duration"]

    # Update the day
    for key, value in data.items():
        if key not in allowed_keys:
            abort(400, description=f"Bad Request: Invalid key {key}")
        setattr(day, key, value)

    # Save the day to the database
    db.session.commit()

    # Return the day as a json object
    return jsonify(day.to_dict()), 200


@views_bp.route('/plans/<int:plan_id>/days/<int:day_id>', methods=['DELETE'], strict_slashes=False)
def remove_day_from_plan(plan_id, day_id):
    """ Remove a single day from a specific plan """

    plan = db.session.get(Plan, plan_id)

    if not plan:
        return abort(404, description="Plan not found")

    day = db.session.get(Day, day_id)

    if not day:
        return abort(404, description="Day not found")

    # Remove the day from the database
    db.session.delete(day)

    # Save the changes to the database
    db.session.commit()

    return jsonify({"message": "Day deleted successfully"}), 200