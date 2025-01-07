#!/usr/bin/env python3
"""
    Create the table schema for roles implementing Role-Based Access Control
    (RBAC)
    """

from models.base import db, BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String


user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True)
)


class Role(BaseModel, db.Model):
    """
        the role class that maps to the roles table in the MySQL database
        """
    __tablename__ = "roles"
    id: Mapped[int] = db.mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True)
    name: Mapped[str] = db.mapped_column(String(50), nullable=False, unique=True)
    users: Mapped["User"] = db.relationship("User", secondary=user_roles, back_populates="roles")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_dict(self):
        return super().to_dict()

    @classmethod
    def find_role_by_name(cls, name):
        query = db.select(cls).where(cls.name == name)
        role = db.session.execute(query).scalar_one_or_none()
        return role
