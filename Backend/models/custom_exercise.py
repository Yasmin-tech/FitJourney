#!/usr/bin/env python3
"""
    Create the table schema for the custom exercises
    that the user creates using sqlalchemy
    """


from models.base import BaseModel, db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey, Float, Table
from datetime import datetime
from typing import Optional, List


class CustomExercise(BaseModel, db.Model):
    """ 
        the custom exercise class that maps to the custom exercises table in the MySQL database
        """
    __tablename__ = "custom_exercises"
    id: Mapped[int] = db.mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True)
    title: Mapped[str] = db.mapped_column(String(128), nullable=False)
    description: Mapped[str] = db.mapped_column(String(255), nullable=True)
    category: Mapped[str] = db.mapped_column(String(128), nullable=False)
    muscle_group: Mapped[str] = db.mapped_column(String(128), nullable=True)
    equipment: Mapped[str] = db.mapped_column(String(128), nullable=True)
    # video_url: Mapped[Optional[str]] = db.mapped_column(String(255), nullable=True)
    media_file_url: Mapped[Optional[str]] = db.mapped_column(String(255), nullable=True)
    workout_sessions: Mapped[List["WorkoutSession"]] = relationship("WorkoutSession", secondary="workout_sessions_custom_exercises", back_populates="custom_exercises")
    user_id: Mapped[int] = db.mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="custom_exercises")
    records: Mapped[List["Record"]] = relationship("Record", back_populates="custom_exercise")


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
