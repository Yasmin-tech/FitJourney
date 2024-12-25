#!/usr/bin/env python3
"""
    Create the table schema for records of workout_sessions using sqlalchemy
    """


from models.base import BaseModel, db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey, Float
from datetime import datetime
from typing import Optional, List


time_format = "%Y-%m-%d %H:%M"


class Record(BaseModel, db.Model):
    """ 
        the record class that maps to the records table in the MySQL database
        """
    __tablename__ = "records"
    id: Mapped[int] = db.mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True)
    _difficulty: Mapped[int] = db.mapped_column(Integer, nullable=False)
    _sets: Mapped[int] = db.mapped_column(Integer, nullable=False)
    _reps: Mapped[int] = db.mapped_column(Integer, nullable=False)
    _rest: Mapped[float] = db.mapped_column(Float, nullable=False)
    _weight_lifted: Mapped[float] = db.mapped_column(Float, nullable=True)
    _user_weight: Mapped[float] = db.mapped_column(Float, nullable=False)
    location: Mapped[str] = db.mapped_column(String(128), nullable=False)
    notes: Mapped[str] = db.mapped_column(String(255), nullable=True)
    user_id: Mapped[int] = db.mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="records")
    exercise_id: Mapped[int] = db.mapped_column(Integer, ForeignKey("exercises.id"), nullable=True)
    custom_exercise_id: Mapped[int] = db.mapped_column(Integer, ForeignKey("custom_exercises.id"), nullable=True)
    exercise: Mapped["Exercise"] = relationship("Exercise", back_populates="records")
    custom_exercise: Mapped["CustomExercise"] = relationship("CustomExercise", back_populates="records")
    date: Mapped[datetime] = db.mapped_column(DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.date = datetime.utcnow()
    
    @property
    def difficulty(self):
        return self._difficulty
    
    @difficulty.setter
    def difficulty(self, value):
        self._difficulty = int(value)

    @property
    def sets(self):
        return self._sets
    
    @sets.setter
    def sets(self, value):
        self._sets = int(value)
    
    @property
    def reps(self):
        return self._reps
    
    @reps.setter
    def reps(self, value):
        self._reps = int(value)
    
    @property
    def rest(self):
        return self._rest

    @rest.setter
    def rest(self, value):
        self._rest = float(value)
    
    @property
    def weight_lifted(self):
        return self._weight_lifted
    
    @weight_lifted.setter
    def weight_lifted(self, value):
        self._weight_lifted = float(value)
    
    @property
    def user_weight(self):
        return self._user_weight
    
    @user_weight.setter
    def user_weight(self, value):
        self._user_weight = float(value)


    def to_dict(self, time_format=time_format):
        new_dict = super().to_dict(time_format)
        new_dict["difficulty"] = self.difficulty
        new_dict["date"] = self.date.strftime(time_format)
        new_dict["sets"] = self._sets
        new_dict["reps"] = self._reps
        new_dict["rest"] = self._rest
        new_dict["weight_lifted"] = self._weight_lifted
        new_dict["user_weight"] = self._user_weight

        del new_dict["_difficulty"]
        del new_dict["_sets"]
        del new_dict["_reps"]
        del new_dict["_rest"]
        del new_dict["_weight_lifted"]
        del new_dict["_user_weight"]

        return new_dict
