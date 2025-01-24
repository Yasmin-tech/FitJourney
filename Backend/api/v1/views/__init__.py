#!/usr/bin/env python3


from flask import Blueprint


views_bp = Blueprint("views_bp", __name__, url_prefix="/api/v1")

from .users import *
from .plans import *
from .days import *
from .exercises import *
from .custom_exercises import *
from .records import *
from .workout_sessions import *
from .roles import *
