#!/usr/bin/env python3
"""
    Create the table schema for plans using sqlalchemy
    """


from models.base import db, BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey, Float
from datetime import datetime
from typing import Optional, List


class Plan(BaseModel, db.Model):
    """
    the plan class that maps to the plans table in the MySQL database
    """

    __tablename__ = "plans"
    id: Mapped[int] = db.mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = db.mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    goal: Mapped[str] = db.mapped_column(String(255), nullable=False)
    _current_weight: Mapped[float] = db.mapped_column(Float, nullable=False)
    _target_weight: Mapped[float] = db.mapped_column(Float, nullable=False)
    _duration: Mapped[int] = db.mapped_column(Integer, nullable=False)
    _days_in_week: Mapped[int] = db.mapped_column(Integer, nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="plans")
    days: Mapped[List["Day"]] = relationship(
        "Day", back_populates="plan", cascade="all, delete-orphan"
    )
    created_at: Mapped[datetime] = db.mapped_column(DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.created_at = datetime.utcnow()

    @property
    def current_weight(self):
        return self._current_weight

    @current_weight.setter
    def current_weight(self, value: str) -> None:
        """Set the current weight as a float  value"""
        self._current_weight = float(value)

    @property
    def target_weight(self):
        return self._target_weight

    @target_weight.setter
    def target_weight(self, value: str) -> None:
        """Set the target weight as a float  value"""
        self._target_weight = float(value)

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value: str) -> None:
        """Set the current duration as an int  value"""
        self._duration = int(value)

    @property
    def days_in_week(self):
        return self._days_in_week

    @days_in_week.setter
    def days_in_week(self, value: str) -> None:
        """Set the days in week as an int  value"""
        self._days_in_week = int(value)

    def to_dict(self):
        # use the getter properties to access private variables
        new_dict = super().to_dict()
        new_dict["current_weight"] = self.current_weight
        new_dict["target_weight"] = self.target_weight
        new_dict["duration"] = self.duration
        new_dict["days_in_week"] = self.days_in_week

        del new_dict["_current_weight"]
        del new_dict["_target_weight"]
        del new_dict["_duration"]
        del new_dict["_days_in_week"]

        return new_dict
