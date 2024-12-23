#!/usr/bin/python3
"""
    Organize error handlers for the app
    """

from flask import Blueprint, jsonify

errors_bp = Blueprint('errors_bp', __name__)


@errors_bp.app_errorhandler(404)
def not_found(error):
    message = "Resource not found"

    if error.description:
        message = error.description
    return jsonify({"error": message}), 404

@errors_bp.app_errorhandler(400)
def bad_request(error):
    message = "Bad Request"

    if error.description:
        message = error.description
    return jsonify({"error": message}), 400
