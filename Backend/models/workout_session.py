#!/usr/bin/env python3
"""
    Create the table schema for workout sessions of exercises using sqlalchemy
    """


from models.base import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey, Float, Table, Column
from datetime import datetime
from typing import Optional, List


# Manage many-to-many relationships btween workout_sessions and exercises
# through an association table
workout_sessions_exercises = Table("workout_sessions_exercises", db.metadata,
    Column("workout_session_id", Integer, ForeignKey('workout_sessions.id', ondelete='CASCADE'), primary_key=True),
    Column("exercise_id", Integer, ForeignKey("exercises.id"), primary_key=True)
)


# Manage many-to-many relationships btween workout_sessions and custom exercises
# created by thr user through an association table
workout_sessions_custom_exercises = Table("workout_sessions_custom_exercises", db.metadata,
    Column("workout_session_id", Integer, ForeignKey('workout_sessions.id', ondelete='CASCADE'), primary_key=True),
    Column("custom_exercise_id", Integer, ForeignKey("custom_exercises.id"), primary_key=True)
)


class WorkoutSession(db.Model):
    """ 
        the workout_session class that maps to the workout_sessions
        table in the MySQL database
        """
    __tablename__ = "workout_sessions"
    id: Mapped[int] = db.mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True)
    day_id: Mapped[int] = db.mapped_column(Integer, ForeignKey("days.id"), nullable=False)
    sets: Mapped[int] = db.mapped_column(Integer, nullable=False)
    reps: Mapped[int] = db.mapped_column(Integer, nullable=False)
    rest: Mapped[float] = db.mapped_column(Float, nullable=False)
    weight_lifted: Mapped[float] = db.mapped_column(Float, nullable=True)
    exercises: Mapped[List["Exercise"]] = relationship("Exercise", secondary=workout_sessions_exercises, back_populates="workout_sessions")
    custom_exercises: Mapped[List["CustomExercise"]] = relationship("CustomExercise", secondary=workout_sessions_custom_exercises, back_populates="workout_sessions")
    day: Mapped["Day"] = relationship("Day", back_populates="workout_sessions")
