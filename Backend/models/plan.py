#!/usr/bin/env python3
"""
    Create the table schema for plans using sqlalchemy
    """


from models.base import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey, Float
from datetime import datetime
from typing import Optional, List


class Plan(db.Model):
    """ 
        the plan class that maps to the plans table in the MySQL database
        """
    __tablename__ = "plans"
    id: Mapped[int] = db.mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True)
    user_id: Mapped[int] = db.mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    goal: Mapped[str] = db.mapped_column(String(255), nullable=False)
    current_weight: Mapped[float] = db.mapped_column(Float, nullable=False)
    target_weight: Mapped[float] = db.mapped_column(Float, nullable=False)
    duration: Mapped[int] = db.mapped_column(Integer, nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="plans")
    days: Mapped[List["Day"]] = relationship("Day", back_populates="plan", cascade="all, delete-orphan")
    created_at: Mapped[datetime] = db.mapped_column(DateTime, default=datetime.utcnow)

