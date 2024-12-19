#!/usr/bin/env python3
"""
    Create the table schema for users using sqlalchemy
    """


from models.base import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime
from datetime import datetime
from typing import Optional, List


class User(db.Model):
    """ 
        the user class that maps to the users table in the MySQL database
        """
    __tablename__ = "users"
    id: Mapped[int] = db.mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True)
    first_name: Mapped[str] = db.mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = db.mapped_column(String(50), nullable=False)
    email: Mapped[str] = db.mapped_column(String(120), nullable=False, unique=True)
    password_hashed: Mapped[str] = db.mapped_column(String(128), nullable=False)
    profile_picture: Mapped[Optional[str]] = db.mapped_column(String(255), nullable=True)
    plans: Mapped[List["Plan"]] = relationship("Plan", back_populates="user", cascade="all, delete-orphan")
    custom_exercises: Mapped[List["CustomExercise"]] = relationship("CustomExercise", back_populates="user", cascade="all, delete-orphan")
    records: Mapped[List["Record"]] = relationship("Record", back_populates="user", cascade="all, delete-orphan")
    created_at: Mapped[datetime] = db.mapped_column(DateTime, default=datetime.utcnow)

