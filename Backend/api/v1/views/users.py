#!/usr/bin/env python3

from . import views_bp
from models.base import db
from models.user import User


@views_bp.route('/users', methods=['GET'])
def get_users():
    return "GET users"
