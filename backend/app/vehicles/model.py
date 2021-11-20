# Standard library imports
from typing import List

# App related imports
from app import session
from app.entities.vehicle import Vehicle

def create_vehicle(name: str, capacity: int, carrier: int) -> None:
    """Add vehicle to database

    :param name:        Vehicle name
    :param capacity:    Vehicle capacity
    """
    user = Vehicle(name=name, capacity=capacity, carrier_id=carrier)
    session.add(user)
    session.commit()
    
def get_vehicle(id: int) -> Vehicle:
    """Get vehicle from database

    :param id:  Vehicle id
    """
    return Vehicle.query.get(id)

def delete_vehicle(id: int) -> None:
    """Delete vehicle from database

    :param id:  Vehicle id
    """
    session.delete(Vehicle.query.get(id))
    session.commit()

def get_vehicles(carrier: int = None) -> List[Vehicle]:
    """Get vehicles from database
    """
    if carrier == None:
        return Vehicle.query.all()
    
    return Vehicle.query.filter(Vehicle.carrier_id == carrier).all()