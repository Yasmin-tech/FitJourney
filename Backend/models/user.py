#!/usr/bin/env python3
"""
    Create the table schema for users using sqlalchemy
    """


from models.base import db, BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime
from datetime import datetime
from typing import Optional, List
import bcrypt


class User(BaseModel, db.Model):
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
    roles: Mapped[List["Role"]] = relationship("Role", secondary="user_roles", back_populates="users")
    created_at: Mapped[datetime] = db.mapped_column(DateTime, default=datetime.utcnow)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = kwargs.get("password")
        self.created_at = datetime.utcnow()

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hashed = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()).decode("utf-8")
    
    def check_password(self, password):
        # Check if the password passed by the user, matches the password in the database
        return bcrypt.checkpw(password.encode("utf-8"), self.password_hashed.encode("utf-8"))
    
    def to_dict(self):
        # Delete the password_hashed from the dictionary before returning it
        new_dict = super().to_dict()
        del new_dict["password_hashed"]
        return new_dict
    
    def is_admin(self):
        # Check if the user is an admin
        return any([role.name == "Admin" for role in self.roles])

    @classmethod
    def find_user_by_email(cls, email):
        """
            Find a user by email
            """
        query = db.select(cls).where(cls.email == email)
        user = db.session.execute(query).scalar_one_or_none()
        return user
