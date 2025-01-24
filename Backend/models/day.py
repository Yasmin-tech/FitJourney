#!/usr/bin/env python3
"""
    Create the table schema for days of exercises using sqlalchemy
    """


from models.base import BaseModel, db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey, Float
from datetime import datetime
from typing import Optional, List


class Day(BaseModel, db.Model):
    """
    the day class that maps to the days table in the MySQL database
    """

    __tablename__ = "days"
    id: Mapped[int] = db.mapped_column(Integer, primary_key=True, autoincrement=True)
    plan_id: Mapped[int] = db.mapped_column(
        Integer, ForeignKey("plans.id"), nullable=False
    )
    title: Mapped[str] = db.mapped_column(String(128), nullable=False)
    _session_duration: Mapped[int] = db.mapped_column(Integer, nullable=True)
    workout_sessions: Mapped[List["WorkoutSession"]] = relationship(
        "WorkoutSession", back_populates="day", cascade="all, delete-orphan"
    )
    plan: Mapped["Plan"] = relationship("Plan", back_populates="days")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def session_duration(self):
        return self._session_duration

    @session_duration.setter
    def session_duration(self, value: str) -> None:
        """Set the session duration as an int  value"""
        self._session_duration = int(value)

    def to_dict(self):
        new_dict = super().to_dict()
        new_dict["session_duration"] = self.session_duration

        del new_dict["_session_duration"]

        return new_dict
