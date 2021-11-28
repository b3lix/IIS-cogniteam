# Standard library imports
import datetime
from os import name
from typing import List

# Flask related imports
from flask import request
from flask_login.utils import logout_user
from flask_pydantic import validate
from flask_login import current_user

# Pydantic related imports
from pydantic import BaseModel, constr, confloat, conint

# App related imports
from app import make_response, session
from app.routes import bp
from app.auth.model import authorization
from app.users.model import get_user, get_staff_instance
from app.routes.model import get_routes, get_route, delete_route
from app.stations.model import get_station
from app.vehicles.model import get_vehicle
from app.entities.user import User, UserType, Staff
from app.entities.route import Route, RouteStop, RouteTime
from app.entities.station import Station
from app.entities.vehicle import Vehicle

class CreateStopForm(BaseModel):
    station: conint(ge=0)
    arrival: conint(ge=0)
    departure: conint(ge=0)

class CreateTimeForm(BaseModel):
    vehicle: conint(ge=0)
    time: datetime.time
    repeat: List[bool]

class CreateForm(BaseModel):
    carrier: conint(ge=0)
    name: constr(strip_whitespace=True, min_length=1)
    price: confloat(ge=0)
    stops: List[CreateStopForm]
    times: List[CreateTimeForm]

@bp.route("/get", methods=["GET"])
@authorization([UserType.admin, UserType.carrier, UserType.staff])
def get_all():
    carrier = None

    if current_user.type == UserType.carrier:
        carrier = current_user.id
    elif current_user.type == UserType.staff:
        staff: Staff = get_staff_instance(current_user.id)

        if staff == None:
            return make_response(401)

        carrier = staff.carrier_id

    return make_response(200, {
        "routes": [{
            "id": route.id,
            "price": route.price,
            "name": route.name,
            "stops": len(route.stops),
            "carrier": {
                "id": route.carrier.id,
                "name": route.carrier.name,
            }
        } for route in get_routes(carrier)] 
    })

@bp.route("/get/<id>", methods=["GET"])
@authorization([UserType.admin, UserType.carrier, UserType.staff])
def get_one(id: int):
    route: Route = get_route(id)

    if route == None:
        return make_response(404)

    # Carrier can fetch only own routes
    if current_user.type == UserType.carrier and current_user.id != route.carrier_id:
        return make_response(401)

    if current_user.type == UserType.staff:
        staff: Staff = get_staff_instance(current_user.id)

        if staff == None or staff.carrier_id != route.carrier_id:
            return make_response(401)

    stops = []
    times = []

    for stop in route.stops:
        stops.append({
            "id": stop.id,
            "arrival": stop.arrival,
            "departure": stop.departure,
            "station": stop.station_id
        })

    for time in route.times:
        times.append({
            "id": time.id,
            "time": str(time.time),
            "repeat": time.repeat,
            "vehicle": time.vehicle_id
        })

    return make_response(200, data={
        "id": route.id,
        "price": route.price,
        "name": route.name,
        "carrier": route.carrier_id,
        "stops": stops,
        "times": times
    })

@bp.route("/delete/<id>", methods=["POST"])
@authorization([UserType.admin, UserType.carrier])
def delete(id: int):
    route: Route = get_route(id)

    if route == None:
        return make_response(404)

    # Carrier can delete only own routes
    if current_user.type == UserType.carrier and current_user.id != route.carrier_id:
        return make_response(401)

    delete_route(id)
    return make_response(200)

@bp.route("/create", methods=["POST"])
@authorization([UserType.admin, UserType.carrier])
@validate()
def create(body: CreateForm):
    if current_user.type == UserType.carrier:
        body.carrier = current_user.id

    # Routes have to be registered to carrier
    user: User = get_user(body.carrier)
    if user == None or user.type != UserType.carrier:
        return make_response(409)

    if len(body.stops) < 2:
        return make_response(500, data={"message": "Počet zastávok musí byť väčší ako 1"})

    if len(body.times) == 0:
        return make_response(500, data={"message": "Zoznam časov je prázdny"})

    # Route name is unique
    if Route.query.filter_by(name = body.name).first() != None:
        return make_response(409, data={"message": "Názov spoju musí byť unikátny"})

    route: Route = Route(carrier_id=body.carrier, name=body.name, price=body.price)
    stops = []
    times = []

    # Create objects and verify data
    previousItem = None
    for item in body.stops:
        station: Station = get_station(item.station)

        if station == None:
            return make_response(409)

        if item.arrival > item.departure:
            return make_response(409, data={"message": "Čas príchodu musí byť menší/rovný ako čas odchodu"})

        if previousItem != None and item.arrival < previousItem.departure:
            return make_response(409, data={"message": "Čas príchodu musí byť väčší/rovný ako čas odchodu na predošlej zastávke"})

        stop: RouteStop = RouteStop(arrival=item.arrival, departure=item.departure, station_id=item.station)
        stops.append(stop)

        previousItem = stop

    for item in body.times:
        if len(item.repeat) != 7:
            return make_response(500)

        vehicle: Vehicle = get_vehicle(item.vehicle)

        # Vehicle must be owned by route carrier owner
        if vehicle == None or vehicle.carrier_id != body.carrier:
            return make_response(409)

        time: RouteTime = RouteTime(time=item.time, repeat=item.repeat, vehicle_id=item.vehicle)
        times.append(time)

    unique_stops = set([ stop.station_id for stop in stops ])
    unique_times = set([ (time.vehicle_id, time.time) for time in times ])

    # Check if there are no duplicate items
    if len(unique_stops) != len(stops) or len(unique_times) != len(times):
        return make_response(409, data={"message": "V spoji sa nachádzajú duplicitné zastávky"})

    # Add route to database
    session.add(route)
    session.flush()
    session.refresh(route)
    for stop in stops:
        stop.route_id = route.id
        session.add(stop)
    for time in times:
        time.route_id = route.id
        session.add(time)
    session.commit()

    return make_response(200)

@bp.route("/update/<id>", methods=["POST"])
@authorization([UserType.admin, UserType.carrier])
@validate()
def update(id: int, body: CreateForm):
    if current_user.type == UserType.carrier:
        body.carrier = current_user.id

    # Routes have to be registered to carrier
    user: User = get_user(body.carrier)
    if user == None or user.type != UserType.carrier:
        return make_response(409)

    if len(body.stops) < 2:
        return make_response(500, data={"message": "Počet zastávok musí byť väčší ako 1"})

    if len(body.times) == 0:
        return make_response(500, data={"message": "Zoznam časov je prázdny"})

    route: Route = get_route(id)
    if route == None:
        return make_response(404)

    # Carrier can update only own routes
    if current_user.type == UserType.carrier and current_user.id != route.carrier_id:
        return make_response(401)

    # Route name is unique
    if route.name != body.name:
        if Route.query.filter_by(name = body.name).first() != None:
            return make_response(409, data={"message": "Názov spoju musí byť unikátny"})

    stops = []
    times = []

    # Create objects and verify data
    previousItem = None
    for item in body.stops:
        station: Station = get_station(item.station)

        if station == None:
            return make_response(409)

        if item.arrival > item.departure:
            return make_response(409, data={"message": "Čas príchodu musí byť menší/rovný ako čas odchodu"})

        if previousItem != None and item.arrival < previousItem.departure:
            return make_response(409, data={"message": "Čas príchodu musí byť väčší/rovný ako čas odchodu na predošlej zastávke"})

        stop: RouteStop = RouteStop(arrival=item.arrival, departure=item.departure, station_id=item.station, route_id=route.id)
        stops.append(stop)

        previousItem = stop

    for item in body.times:
        if len(item.repeat) != 7:
            return make_response(500)

        vehicle: Vehicle = get_vehicle(item.vehicle)

        # Vehicle must be owned by route carrier owner
        if vehicle == None or vehicle.carrier_id != body.carrier:
            return make_response(409)

        time: RouteTime = RouteTime(time=item.time, repeat=item.repeat, vehicle_id=item.vehicle, route_id=route.id)
        times.append(time)

    unique_stops = set([ stop.station_id for stop in stops ])
    unique_times = set([ (time.vehicle_id, time.time) for time in times ])

    # Check if there are no duplicate items
    if len(unique_stops) != len(stops) or len(unique_times) != len(times):
        return make_response(409, data={"message": "V spoji sa nachádzajú duplicitné zastávky"})

    route.name = body.name
    route.price = body.price
    RouteStop.query.filter(RouteStop.route_id == route.id).delete()
    RouteTime.query.filter(RouteTime.route_id == route.id).delete()
    for stop in stops:
        session.add(stop)
    for time in times:
        session.add(time)
    session.commit()

    return make_response(200)