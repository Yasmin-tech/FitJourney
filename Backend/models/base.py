#!/usr/bin/env python3
"""
    The base model to create an instance of SQLAlchemy
    """


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


class Base(DeclarativeBase, MappedAsDataclass):
    """
         Provide the bases classes the app's models
         """
    pass


db = SQLAlchemy(model_class=Base)

