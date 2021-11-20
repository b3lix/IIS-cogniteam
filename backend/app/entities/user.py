# Standard library imports
import enum

# Flask related imports
from flask_login import UserMixin

# SQLalchemy related imports
from sqlalchemy import Column, String, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.functions import user

# App related imports
from app.entities import Base

class UserType(enum.IntEnum):
    passenger = 0
    staff = 1
    carrier = 2
    admin = 3

class User(UserMixin, Base):
    __tablename__  = "users"
    id: int        = Column(Integer, primary_key = True, autoincrement = True)
    username: str  = Column(String(64), index = True, unique = True)
    password: str  = Column(String(128))
    email: str     = Column(String(128))
    name: str      = Column(String(128))
    type: UserType = Column(Enum(UserType), default = UserType.passenger)

class Staff(Base):
    __tablename__   = "staff"
    user_id: int    = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key = True, nullable=False, index=True)
    carrier_id: int = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key = True, nullable=False, index=True)