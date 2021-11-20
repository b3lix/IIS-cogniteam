# Standard library imports
from typing import List
from datetime import time

# SQLalchemy related imports
from sqlalchemy import Column, String, Integer, Enum, Boolean, ForeignKey, Time, ARRAY, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null

# App related imports
from app.entities import Base
from app.entities.user import User
from app.entities.vehicle import Vehicle
from app.entities.station import Station

class Route(Base):
    __tablename__    = "routes"
    id: int          = Column(Integer, primary_key = True, autoincrement = True)
    name: str        = Column(String, nullable=False)
    price: float     = Column(Float)
    carrier_id: int  = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    stops            = relationship("RouteStop", backref="parent", passive_deletes=True)
    times            = relationship("RouteTime", backref="parent", passive_deletes=True)

    carrier: User    = relationship(User)

class RouteTime(Base):
    __tablename__    = "route_times"
    id: int             = Column(Integer, primary_key=True, autoincrement = True)
    time: time          = Column(Time)
    repeat: List[bool]  = Column(ARRAY(Boolean))
    
    route_id: int       = Column(Integer, ForeignKey("routes.id", ondelete="CASCADE"), nullable=False)
    vehicle_id: int     = Column(Integer, ForeignKey("vehicles.id", ondelete="CASCADE"), nullable=False)

    vehicle: Vehicle    = relationship(Vehicle, foreign_keys=[vehicle_id])
    #route: Route        = relationship(Route, foreign_keys=[route_id])

class RouteStop(Base):
    __tablename__    = "route_stops"
    id: int          = Column(Integer, primary_key=True, autoincrement = True)
    arrival: time    = Column(Integer)
    departure: time  = Column(Integer)
    
    route_id: int    = Column(Integer, ForeignKey("routes.id", ondelete="CASCADE"), nullable=False)
    station_id: int  = Column(Integer, ForeignKey("stations.id", ondelete="CASCADE"), nullable=False)

    station: Station = relationship(Station, foreign_keys=[station_id])
    #route: Route     = relationship(Route, foreign_keys=[route_id])