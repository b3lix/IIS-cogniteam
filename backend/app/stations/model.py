# Standard library imports
from typing import List

# App related imports
from app import session
from app.entities.station import StationUpdate, Station, StationUpdateType

def create_station_update(name: str, location: str, original: int, author: int, type: StationUpdateType) -> None:
    """Add insert station update to database

    :param name:        Station name
    :param location:    Station location
    :param original:    Original station data
    :param author:      Author of the update
    :param type:        Update type
    """
    update = StationUpdate(name=name, location=location, original_station_id=original, author_id=author, type=type)
    session.add(update)
    session.commit()

def create_station(name: str, location: str) -> None:
    """Add station to database

    :param name:        Station name
    :param location:    Station location
    """
    station = Station(name=name, location=location)
    session.add(station)
    session.commit()

def update_station(id: int, name: str, location: str) -> None:
    """Update station in database

    :param id:          Station ID
    :param name:        Station name
    :param location:    Station location
    """
    station: Station = Station.query.get(id)
    station.name = name
    station.location = location
    session.commit()

def get_station(id: int) -> Station:
    """Get station from database
    """
    return Station.query.get(id)

def delete_station(id: int) -> None:
    """Delete station from database

    :param id:  Station id
    """
    session.delete(Station.query.get(id))
    session.commit()

def get_stations() -> List[Station]:
    """Get stations from database
    """
    return Station.query.all()

def get_station_update(id: int) -> StationUpdate:
    """Get station update from database

    :param id:  Update ID
    """
    return StationUpdate.query.get(id)

def get_station_updates() -> List[StationUpdate]:
    """Get station updates from database
    """
    return StationUpdate.query.all()

def approve_station_update(id: int) -> None:
    """Approve station update

    :param id:  Update ID
    """
    update: StationUpdate = StationUpdate.query.get(id)

    if update.type == StationUpdateType.update:
        update_station(update.original_station_id, update.name, update.location, update.type)
    elif update.type == StationUpdateType.insert:
        create_station(update.name, update.location, update.type)
    elif update.type == StationUpdateType.delete:
        session.delete(Station.query.get(update.original_station_id))
        session.commit()
        return
    
    session.delete(update)
    session.commit()

def delete_station_update(id: int) -> None:
    """Remove station update from database

    :param id:  Update ID
    """
    session.delete(StationUpdate.query.get(id))
    session.commit()