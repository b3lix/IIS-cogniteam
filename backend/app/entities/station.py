# Standard library imports
import enum

# SQLalchemy related imports
from sqlalchemy import Column, String, Integer, Enum, Boolean, ForeignKey
from sqlalchemy.orm import relationship

# App related imports
from app.entities import Base
from app.entities.user import User

class Station(Base):
    __tablename__       = "stations"
    id: int             = Column(Integer, primary_key = True, autoincrement = True)
    name: str           = Column(String(64))
    location: str       = Column(String(64))

class StationUpdateType(enum.IntEnum):
    insert = 0
    update = 1
    delete = 2

class StationUpdate(Base):
    __tablename__                   = "station_updates"
    id: int                         = Column(Integer, primary_key = True, autoincrement = True)
    name: str                       = Column(String(64), nullable=True)
    location: str                   = Column(String(64), nullable=True)
    type: StationUpdateType         = Column(Enum(StationUpdateType))

    original_station_id: int        = Column(Integer, ForeignKey("stations.id", ondelete="CASCADE"), nullable = True)
    author_id: int                  = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable = False)

    original_station: Station       = relationship(Station, foreign_keys=[original_station_id])
    author: User                    = relationship(User, foreign_keys=[author_id])