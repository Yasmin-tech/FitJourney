#!/usr/bin/env python3
"""
    Create the table schema for records of workout_sessions using sqlalchemy
    """


from models.base import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey, Float
from datetime import datetime
from typing import Optional, List


class Record(db.Model):
    """ 
        the record class that maps to the records table in the MySQL database
        """
    __tablename__ = "records"
    id: Mapped[int] = db.mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True)
    difficulty: Mapped[int] = db.mapped_column(Integer, nullable=False)
    sets: Mapped[int] = db.mapped_column(Integer, nullable=False)
    reps: Mapped[int] = db.mapped_column(Integer, nullable=False)
    rest: Mapped[float] = db.mapped_column(Float, nullable=False)
    weight_lifted: Mapped[float] = db.mapped_column(Float, nullable=True)
    user_weight: Mapped[float] = db.mapped_column(Float, nullable=False)
    location: Mapped[str] = db.mapped_column(String(128), nullable=False)
    notes: Mapped[str] = db.mapped_column(String(255), nullable=True)
    user_id: Mapped[int] = db.mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="records")
    exercise_id: Mapped[int] = db.mapped_column(Integer, ForeignKey("exercises.id"), nullable=True)
    custom_exercise_id: Mapped[int] = db.mapped_column(Integer, ForeignKey("custom_exercises.id"), nullable=True)
    exercise: Mapped["Exercise"] = relationship("Exercise", back_populates="records")
    custom_exercise: Mapped["CustomExercise"] = relationship("CustomExercise", back_populates="records")
    date: Mapped[datetime] = db.mapped_column(DateTime, default=datetime.utcnow)
