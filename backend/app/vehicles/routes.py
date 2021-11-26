# Standard library imports
from os import stat
from typing import List

# Flask related imports
from flask import request
from flask_login.utils import logout_user
from flask_pydantic import validate
from flask_login import current_user

# Pydantic related imports
from pydantic import BaseModel, constr, conint

# App related imports
from app import make_response, session
from app.vehicles import bp
from app.auth.model import authorization
from app.users.model import get_user, get_user, get_staff_instance
from app.stations.model import get_station
from app.vehicles.model import create_vehicle, get_vehicle, get_vehicles, delete_vehicle
from app.entities.vehicle import Vehicle
from app.entities.user import User, UserType, Staff
from app.entities.station import Station

class CreateForm(BaseModel):
    name: constr(strip_whitespace=True, min_length=3)
    capacity: conint(ge=1)
    carrier: conint(ge=0)

@bp.route("/create", methods=["POST"])
@authorization([UserType.admin, UserType.carrier])
@validate()
def create(body: CreateForm):
    if current_user.type == UserType.carrier:
        body.carrier = current_user.id

    # Vehicles can be registered only to carriers
    user: User = get_user(body.carrier)
    if user == None or user.type != UserType.carrier:
        return make_response(409)

    create_vehicle(body.name, body.capacity, body.carrier)
    return make_response(200)

@bp.route("/delete/<id>", methods=["POST"])
@authorization([UserType.admin, UserType.carrier])
def delete(id: int):
    vehicle: Vehicle = get_vehicle(id)

    if vehicle == None:
        return make_response(404)

    # Carrier can delete only own vehicles
    if current_user.type == UserType.carrier and current_user.id != vehicle.carrier_id:
        return make_response(401)

    delete_vehicle(id)
    return make_response(200)

@bp.route("/get/<id>", methods=["GET"])
@authorization([UserType.admin, UserType.carrier, UserType.staff])
def get_one(id: int):
    vehicle: Vehicle = get_vehicle(id)

    if vehicle == None:
        return make_response(404)

    # Carrier can fetch only own vehicles
    if current_user.type == UserType.carrier and current_user.id != vehicle.carrier_id:
        return make_response(401)

    if current_user.type == UserType.staff:
        staff: Staff = get_staff_instance(current_user.id)

        if staff == None or staff.carrier_id != vehicle.carrier_id:
            return make_response(401)

    return make_response(200, data={
        "name": vehicle.name,
        "capacity": vehicle.capacity,
        "carrier": vehicle.carrier.id,
        "station": vehicle.station_id
    })


@bp.route("/get", methods=["GET"])
@authorization([UserType.admin, UserType.carrier, UserType.staff])
def get_all():
    carrier = None if current_user.type == UserType.admin else current_user.id

    if current_user.type == UserType.carrier:
        carrier = current_user.id
    elif current_user.type == UserType.staff:
        staff: Staff = get_staff_instance(current_user.id)

        if staff == None:
            return make_response(401)

        carrier = staff.carrier_id

    return make_response(200, {
        "vehicles": [{
            "id": vehicle.id,
            "name": vehicle.name,
            "capacity": vehicle.capacity,
            "station": vehicle.station_id,
            "carrier": {
                "id": vehicle.carrier.id,
                "name": vehicle.carrier.name,
            }
        } for vehicle in get_vehicles(carrier)] 
    })

@bp.route("/update/<id>", methods=["POST"])
@authorization([UserType.admin, UserType.carrier])
@validate()
def update(id: int, body: CreateForm):
    vehicle: Vehicle = get_vehicle(id)

    if vehicle == None:
        return make_response(404)

    # Carrier can only update own vehicles
    if current_user.type == UserType.carrier and current_user.id != vehicle.carrier_id:
        return make_response(401)

    # Vehicles can be registered only to carriers
    user: User = get_user(body.carrier)
    if user == None or user.type != UserType.carrier:
        return make_response(409)

    vehicle.name = body.name
    vehicle.capacity = body.capacity
    
    if current_user.type == UserType.admin:
        vehicle.carrier_id = body.carrier

    session.commit()
    return make_response(200)
    
@bp.route("/update_station/<vehicle_id>/<station_id>", methods=["POST"])
@authorization([UserType.admin, UserType.staff])
def update_station(vehicle_id: int, station_id: int):
    vehicle: Vehicle = get_vehicle(vehicle_id)
    station: Station = get_station(station_id)

    if vehicle == None or station == None:
        return make_response(404)

    if current_user.type == UserType.staff:
        staff: Staff = get_staff_instance(current_user.id)

        # Staff can only update station of vehicles under its carrier
        if staff == None or staff.carrier_id != vehicle.carrier_id:
            return make_response(401)

    vehicle.station_id = station.id
    session.commit()
    return make_response(200)