#!/usr/bin/env python3
"""
    Create the table schema for workout sessions of exercises using sqlalchemy
    """


from models.base import BaseModel, db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey, Float, Table, Column
from datetime import datetime
from typing import Optional, List


# # Manage many-to-many relationships btween workout_sessions and exercises
# # through an association table
# workout_sessions_exercises = Table("workout_sessions_exercises", db.metadata,
#     Column("workout_session_id", Integer, ForeignKey('workout_sessions.id', ondelete='CASCADE'), primary_key=True),
#     Column("exercise_id", Integer, ForeignKey("exercises.id"), primary_key=True)
# )


# # Manage many-to-many relationships btween workout_sessions and custom exercises
# # created by the user through an association table
# workout_sessions_custom_exercises = Table("workout_sessions_custom_exercises", db.metadata,
#     Column("workout_session_id", Integer, ForeignKey('workout_sessions.id', ondelete='CASCADE'), primary_key=True),
#     Column("custom_exercise_id", Integer, ForeignKey("custom_exercises.id"), primary_key=True)
# )


class WorkoutSession(BaseModel, db.Model):
    """
    the workout_session class that maps to the workout_sessions
    table in the MySQL database
    """

    __tablename__ = "workout_sessions"
    id: Mapped[int] = db.mapped_column(Integer, primary_key=True, autoincrement=True)
    day_id: Mapped[int] = db.mapped_column(
        Integer, ForeignKey("days.id"), nullable=False
    )
    exercise_id: Mapped[int] = db.mapped_column(
        Integer, ForeignKey("exercises.id"), nullable=True
    )
    custom_exercise_id: Mapped[int] = db.mapped_column(
        Integer, ForeignKey("custom_exercises.id"), nullable=True
    )
    _sets: Mapped[int] = db.mapped_column(Integer, nullable=False)
    _reps: Mapped[int] = db.mapped_column(Integer, nullable=False)
    _rest: Mapped[float] = db.mapped_column(Float, nullable=False)
    _weight_lifted: Mapped[float] = db.mapped_column(Float, nullable=True)
    # exercises: Mapped[List["Exercise"]] = relationship("Exercise", secondary=workout_sessions_exercises, back_populates="workout_sessions")
    # custom_exercises: Mapped[List["CustomExercise"]] = relationship("CustomExercise", secondary=workout_sessions_custom_exercises, back_populates="workout_sessions")
    day: Mapped["Day"] = relationship("Day", back_populates="workout_sessions")
    exercise: Mapped["Exercise"] = relationship(
        "Exercise", back_populates="workout_sessions"
    )
    custom_exercise: Mapped["CustomExercise"] = relationship(
        "CustomExercise", back_populates="workout_sessions"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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

    def to_dict(self):
        new_dict = super().to_dict()
        new_dict["sets"] = self.sets
        new_dict["reps"] = self.reps
        new_dict["rest"] = self.rest
        new_dict["weight_lifted"] = self.weight_lifted

        del new_dict["_sets"]
        del new_dict["_reps"]
        del new_dict["_rest"]
        del new_dict["_weight_lifted"]

        return new_dict
