# Standard library imports
from typing import List

# App related imports
from app import session
from app.entities.route import Route

def get_routes(carrier: int = None) -> List[Route]:
    """Get routes from database
    """
    if carrier == None:
        return Route.query.all()
    
    return Route.query.filter(Route.carrier_id == carrier).all()

def get_route(id: int) -> Route:
    """Get route from database

    :param id:  Route id
    """
    return Route.query.get(id)

def delete_route(id: int) -> None:
    """Delete route from database

    :param id:  route id
    """
    session.delete(Route.query.get(id))
    session.commit()
