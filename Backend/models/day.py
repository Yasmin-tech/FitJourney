#!/usr/bin/env python3
"""
    Create the table schema for days of exercises using sqlalchemy
    """


from models.base import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey, Float
from datetime import datetime
from typing import Optional, List


class Day(db.Model):
    """ 
        the day class that maps to the days table in the MySQL database
        """
    __tablename__ = "days"
    id: Mapped[int] = db.mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True)
    plan_id: Mapped[int] = db.mapped_column(Integer, ForeignKey("plans.id"), nullable=False)
    title: Mapped[str] = db.mapped_column(String(128), nullable=False)
    sesion_duration: Mapped[int] = db.mapped_column(Integer, nullable=True)
    workout_sessions: Mapped[List["WorkoutSession"]] = relationship("WorkoutSession", back_populates="day", cascade="all, delete-orphan")
    plan: Mapped["Plan"] = relationship("Plan", back_populates="days")

