# Standard library imports
from datetime import date, datetime

# App related imports
from app.entities import Base

# SQLalchemy related imports
from sqlalchemy import Column, Integer, ForeignKey, Date, Float, Boolean, String, DateTime
from sqlalchemy.orm import relationship

from app.entities.route import RouteTime, RouteStop
from app.entities.user import User

class Seat(Base):
    __tablename__         = "seats"
    id: int               = Column(Integer, primary_key = True, autoincrement = True)
    date: date            = Column(Date)
    amount: int           = Column(Integer)
    price: int            = Column(Float)
    paid: bool            = Column(Boolean, default=False)
    name: str             = Column(String)

    created_at: datetime  = Column(DateTime, default=datetime.utcnow())

    email: str            = Column(String)
    user_id: int          = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    from_stop_id: int     = Column(Integer, ForeignKey("route_stops.id", ondelete="SET NULL"), nullable=True)
    to_stop_id: int       = Column(Integer, ForeignKey("route_stops.id", ondelete="SET NULL"), nullable=True)

    time_id: int          = Column(Integer, ForeignKey("route_times.id", ondelete="SET NULL"), nullable=True)

    from_stop: RouteStop  = relationship(RouteStop, foreign_keys=[from_stop_id])
    to_stop: RouteStop    = relationship(RouteStop, foreign_keys=[to_stop_id])

    time: RouteTime       = relationship(RouteTime, foreign_keys=[time_id])
    user: User            = relationship(User, foreign_keys=[user_id])
