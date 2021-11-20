# SQLalchemy related imports
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from app.entities.user import User, Staff
from app.entities.vehicle import Vehicle
from app.entities.station import Station, StationUpdate
from app.entities.route import Route, RouteStop, RouteTime
from app.entities.seat import Seat