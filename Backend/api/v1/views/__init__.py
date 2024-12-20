#!/usr/bin/env python3


from flask import Blueprint


views_bp = Blueprint('views_bp', __name__, url_prefix='/api/v1')

from .users import *
