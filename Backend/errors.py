#!/usr/bin/python3
"""
    Organize error handlers for the app
    """

from flask import Blueprint, jsonify


errors_bp = Blueprint("errors_bp", __name__)


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


@errors_bp.app_errorhandler(409)
def conflict(error):
    message = "Conflict"

    if error.description:
        message = error.description
    return jsonify({"error": message}), 409


@errors_bp.app_errorhandler(500)
def internal_server_error(error):
    message = "Internal Server Error"

    if error.description:
        message = error.description
    return jsonify({"error": message}), 500


@errors_bp.app_errorhandler(403)
def forbidden(error):
    message = "Forbidden"

    if error.description:
        message = error.description
    return jsonify({"error": message}), 403


if __name__ == "__main__":
    app.run(debug=True)
