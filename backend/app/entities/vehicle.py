# Standard library imports
import enum

# SQLalchemy related imports
from sqlalchemy import Column, String, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null

# App related imports
from app.entities import Base
from app.entities.user import User

class Vehicle(Base):
    __tablename__       = "vehicles"
    id: int             = Column(Integer, primary_key = True, autoincrement = True)
    name: str           = Column(String(64))
    carrier_id: int     = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    capacity: int       = Column(Integer)
    station_id: int     = Column(Integer, ForeignKey("stations.id", ondelete="SET NULL"), nullable=True)

    carrier: User       = relationship(User, foreign_keys=[carrier_id])
    station             = relationship("Station", foreign_keys=[station_id])
