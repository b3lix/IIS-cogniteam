# Standard library imports
from os import stat
from typing import Optional

# Flask related imports
from flask_login import current_user
from flask_pydantic.core import validate

# Pydantic related imports
from pydantic import BaseModel, constr

# App related imports
from app import make_response, session
from app.stations import bp
from app.auth.model import authorization
from app.stations.model import create_station_update, get_stations, get_station_updates, get_station_update, delete_station_update, approve_station_update,\
                                get_station, delete_station, create_station, update_station
from app.entities.user import User, UserType
from app.entities.station import Station, StationUpdate, StationUpdateType

class CreateForm(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)
    location: constr(strip_whitespace=True, min_length=1)

@bp.route("/create", methods=["POST"])
@authorization([UserType.admin, UserType.carrier])
@validate()
def create(body: CreateForm):
    if current_user.type == UserType.admin:
        create_station(body.name, body.location)
    elif current_user.type == UserType.carrier:
        create_station_update(body.name, body.location, None, current_user.id, StationUpdateType.insert)
    return make_response(200)

@bp.route("/delete/<id>", methods=["POST"])
@authorization([UserType.admin, UserType.carrier])
def delete(id: int):
    station: Station = get_station(id)

    if station == None:
        return make_response(404)

    if current_user.type == UserType.admin:
        delete_station(id)
    elif current_user.type == UserType.carrier:
        create_station_update(None, None, None, id, current_user.id, StationUpdateType.delete)
    return make_response(200)

@bp.route("/update/<id>", methods=["POST"])
@authorization([UserType.admin, UserType.carrier])
@validate()
def update(id: int, body: CreateForm):
    station: Station = get_station(id)

    if station == None:
        return make_response(404)
    
    if current_user.type == UserType.admin:
        update_station(id, body.name, body.location)
    elif current_user.type == UserType.carrier:
        create_station_update(body.name, body.location, id, current_user.id, StationUpdateType.update)
    return make_response(200)

@bp.route("/delete_update/<id>", methods=["POST"])
@authorization([UserType.admin])
def delete_update(id: int):
    update: StationUpdate = get_station_update(id)

    if update == None:
        return make_response(404)

    delete_station_update(id)
    return make_response(200)

@bp.route("/approve_update/<id>", methods=["POST"])
@authorization([UserType.admin])
def approve_update(id: int):
    update: StationUpdate = get_station_update(id)

    if update == None:
        return make_response(404)

    approve_station_update(id)
    return make_response(200)

@bp.route("/get_updates", methods=["GET"])
@authorization([UserType.admin])
def get_updates():
     return make_response(200, {
        "updates": [{
            "id": station.id,
            "name": station.name,
            "location": station.location,
            "original_station": {
                "id": station.original_station.id,
                "name": station.original_station.name,
                "location": station.original_station.location,
            } if station.original_station != None else None,
            "author": {
                "id": station.author.id,
                "username": station.author.username,
                "type": station.author.type
            }
        } for station in get_station_updates()] 
    })

@bp.route("/get/<id>", methods=["GET"])
@authorization([UserType.admin, UserType.carrier])
def get_one(id: int):
    station: Station = get_station(id)

    if station == None:
        return make_response(404)

    return make_response(200, data={
        "name": station.name,
        "location": station.location,
    })

@bp.route("/get", methods=["GET"])
def get():
     return make_response(200, {
        "stations": [{
            "id": station.id,
            "name": station.name,
            "location": station.location,
        } for station in get_stations()] 
    })