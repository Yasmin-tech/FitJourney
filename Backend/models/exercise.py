#!/usr/bin/env python3
"""
    Create the table schema for exercises using sqlalchemy
    """


from models.base import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey, Float, Table
from datetime import datetime
from typing import Optional, List


class Exercise(db.Model):
    """ 
        the exercise class that maps to the exercises table in the MySQL database
        """
    __tablename__ = "exercises"
    id: Mapped[int] = db.mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True)
    title: Mapped[str] = db.mapped_column(String(128), nullable=False)
    description: Mapped[str] = db.mapped_column(String(255), nullable=True)
    category: Mapped[str] = db.mapped_column(String(128), nullable=False)
    muscle_group: Mapped[str] = db.mapped_column(String(128), nullable=False)
    equipment: Mapped[str] = db.mapped_column(String(128), nullable=True)
    video_url: Mapped[Optional[str]] = db.mapped_column(String(255), nullable=True)
    img_url: Mapped[Optional[str]] = db.mapped_column(String(255), nullable=True)
    workout_sessions: Mapped[List["WorkoutSession"]] = relationship("WorkoutSession", secondary="workout_sessions_exercises", back_populates="exercises")
    records: Mapped[List["Record"]] = relationship("Record", back_populates="exercise")
