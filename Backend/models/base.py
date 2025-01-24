#!/usr/bin/env python3
"""
    The base model to create an instance of SQLAlchemy
    """


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from datetime import datetime


time_format = "%Y-%m-%d"


class Base(DeclarativeBase, MappedAsDataclass):
    """
    Provide the bases classes the app's models
    """

    pass


db = SQLAlchemy(model_class=Base)


class BaseModel:
    """This will be the base model for all the models in the app
    It will have all basic functions that will be used by all the models
    """

    # Initialize the object with the given keyword arguments
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    # convert the value based to a datetime object
    def to_datetime(self, value, time_format=time_format):
        return datetime.strptime(value, time_format)

    # return a json serializable dictionary
    def to_dict(self, time_format=time_format):
        # new_dict = self.__dict__.copy()
        new_dict = {
            c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs
        }
        for key, value in new_dict.items():
            if isinstance(value, datetime):
                new_dict[key] = value.strftime(time_format)

        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]

        return new_dict

    # @classmethod
    # def get_all(cls):
    #     return cls.query.all()

    # @classmethod
    # def get_by_id(cls, id):
    #     return cls.query.get(id)

    # @classmethod
    # def get_by_name(cls, name):
    #     return cls.query.filter_by(name=name).first()

    # @classmethod
    # def get_by_email(cls, email):
    #     return cls.query.filter_by(email=email).first()

    # @classmethod
    # def get_by_username(cls, username):
    #     return cls.query.filter_by(username=username).first()

    # @classmethod
    # def get_by_phone(cls, phone):
    #     return cls.query.filter_by(phone=phone).first()
