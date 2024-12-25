#!/usr/bin/env python3
""" API endpoints for the plans """

from . import views_bp
from models.base import db
from models.plan import Plan
from models.user import User
from flask import request, jsonify, abort


@views_bp.route('/plans', methods=['GET'], strict_slashes=False)
def get_all_plans():
    """ Retrieve all the plans from the database """
    query = db.select(Plan)
    plans = db.session.execute(query).scalars().all()

    if not plans:
        return jsonify([]), 200
    # Return the plans as a json object
    return jsonify([plan.to_dict() for plan in plans])


@views_bp.route('/plans/<int:plan_id>', methods=['GET'], strict_slashes=False)
def get_one_plan(plan_id):
    """ Retrieve a single plan from the database """
    plan = db.session.get(Plan, plan_id)

    if plan is None:
        return abort(404, description="Plan not found")
    # Return the plan as a json object
    return jsonify(plan.to_dict()), 200


@views_bp.route('/users/<int:user_id>/plans', methods=['GET'], strict_slashes=False)
def get_all_plans_for_user(user_id):
    """ Retrieve all the plans for a specific user """
    user = db.session.get(User, user_id)

    if not user:
        return abort(404, description="User not found")

    # Aceess the plans attribute of the user object
    plans = user.plans
    if not plans:
        return jsonify([]), 200

    # Return the plans as a json object
    return jsonify([plan.to_dict() for plan in plans])


@views_bp.route('/users/<int:user_id>/plans/<int:plan_id>', methods=['GET'], strict_slashes=False)
def get_one_plan_for_user(user_id, plan_id):
    """ Retrieve a single plan for a specific user """
    user = db.session.get(User, user_id)

    if not user:
        return abort(404, description="User not found")

    # Access the plans attribute of the user object
    # This generator expression will return the plan object if the plan_id matches

    plan = next((plan for plan in user.plans if plan.id == plan_id), None)
    if not plan:
        return abort(404, description="Plan not found")

    # Return the plan as a json object
    return jsonify(plan.to_dict())


@views_bp.route('/users/<int:user_id>/plans', methods=['POST'], strict_slashes=False)
def create_plan_for_user(user_id):
    """ Create a new plan for a specific user """

    # Retrieve the user object
    user = db.session.get(User, user_id)

    if not user:
        return abort(404, description="User not found")
    
    data = request.get_json()

    if not data:
        return abort(400, description="Bad Request: Not a JSON")
    
    # Check if the required fields are in the json object
    if "goal" not in data:
        return abort(400, description="Bad Request: Missing goal")
    if "current_weight" not in data:
        return abort(400, description="Bad Request: Missing current_weight")
    if "target_weight" not in data:
        return abort(400, description="Bad Request: Missing target_weight")
    if "duration" not in data:
        return abort(400, description="Bad Request: Missing duration")
    if "days_in_week" not in data:
        return abort(400, description="Bad Request: Missing days_in_week")

    
    # Create a new plan
    new_plan = Plan(**data, user_id=user_id)

    # Save the plan to the database
    db.session.add(new_plan)
    db.session.commit()

    # Add the plan to the user's plans
    user.plans.append(new_plan)

    return jsonify(new_plan.to_dict()), 201


@views_bp.route('/users/<int:user_id>/plans/<int:plan_id>', methods=['PUT'], strict_slashes=False)
def update_plan_for_user(user_id, plan_id):
    """ Update a plan for a specific user """

    # Retrieve the user object
    user = db.session.get(User, user_id)

    if not user:
        return abort(404, description="User not found")
    
    # Access the plans attribute of the user object
    # This generator expression will return the plan object if the plan_id matches
    plan = next((plan for plan in user.plans if plan.id == plan_id), None)

    if not plan:
        return abort(404, description="Plan not found")
    
    data = request.get_json()

    if not data:
        return abort(400, description="Bad Request: Not a JSON")
    
    allowed_keys = ["goal", "current_weight", "target_weight", "duration"]

    # Update the plan with the new data
    for key, value in data.items():
        if key not in allowed_keys:
            return abort(400, description=f"Bad Request: Invalid key {key}")
        setattr(plan, key, value)

    # Save the plan to the database
    db.session.commit()

    return jsonify(plan.to_dict()), 200


@views_bp.route('/users/<int:user_id>/plans/<int:plan_id>', methods=['DELETE'], strict_slashes=False)
def remove_plan_for_user(user_id, plan_id):
    """ Remove a plan for a specific user """

    # Retrieve the user object
    user = db.session.get(User, user_id)

    if not user:
        return abort(404, description="User not found")
    
    # Access the plans attribute of the user object
    # This generator expression will return the plan object if the plan_id matches
    plan = next((plan for plan in user.plans if plan.id == plan_id), None)

    if not plan:
        return abort(404, description="Plan not found")
    
    # Remove the plan from the database
    db.session.delete(plan)
    db.session.commit()

    return jsonify({"message": "Plan deleted successfully"}), 200
