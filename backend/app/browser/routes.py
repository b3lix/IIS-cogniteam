# Standard library imports
from datetime import date, time, datetime, timedelta
from os import name
from typing import List

# Flask related imports
from flask import request
from flask_login import current_user
from flask_pydantic.core import validate

# SQLalchemy related imports
from sqlalchemy import func, cast, Interval, text, or_

# Pydantic related imports
from pydantic import BaseModel, conint, constr
from pydantic.networks import EmailStr

# App related imports
from app import make_response, session
from app.browser import bp
from app.stations.model import get_station
from app.entities.station import Station
from app.entities.route import Route, RouteStop, RouteTime
from app.entities.user import User, UserType, Staff
from app.entities.vehicle import Vehicle
from app.entities.seat import Seat
from app.auth.model import authorization
from app.users.model import get_staff_instance

class FindForm(BaseModel):
    from_station: conint(ge=0)
    to_station: conint(ge=0)
    date: date
    time: time

class CreateForm(BaseModel):
    route: conint(ge=0)
    from_stop: conint(ge=0)
    to_stop: conint(ge=0)
    date: date
    name: constr(strip_whitespace=True, min_length=3)
    email: EmailStr
    amount: conint(ge=1, le=5)

@bp.route("/create_seat", methods=["POST"])
@validate()
def create_seat(body: CreateForm):
    if not current_user.is_authenticated:
        user: User = User.query.filter_by(email = body.email).first()

        if user != None:
            return make_response(409, data={"message": "Túto emailovú adresu už používa registrovaný uživateľ"})

    elif current_user.type != UserType.passenger and current_user.type != UserType.admin:
        return make_response(401)

    time: RouteTime = RouteTime.query \
        .filter(RouteTime.id == body.route) \
        .filter(RouteTime.repeat[func.extract("dow", body.date + RouteTime.time)] == True).first()

    if time == None:
        return make_response(409)

    route: Route = Route.query.get(time.route_id)

    if route == None:
        return make_response(409)

    from_stop: RouteStop = RouteStop.query.get(body.from_stop)
    to_stop: RouteStop = RouteStop.query.get(body.to_stop)

    if from_stop == None or to_stop == None or from_stop.route_id != route.id or to_stop.route_id != route.id:
        return make_response(409)

    # Check if user reached maximum numbers of reservations
    my_seat_condition = []
    my_seat_condition.append(Seat.email == body.email)
    if hasattr(current_user, "type"):
        my_seat_condition.append(Seat.email == current_user.email)
        my_seat_condition.append(Seat.user_id == current_user.id)

    my_seats = session.query(func.sum(Seat.amount)) \
                .filter(Seat.time_id == body.route) \
                .filter(Seat.date == body.date) \
                .filter(Seat.from_stop_id < body.to_stop) \
                .filter(body.from_stop < Seat.to_stop_id) \
                .filter(or_(*my_seat_condition)) \
                .first()

    my_seats = my_seats[0] if my_seats[0] != None else 0

    if my_seats + body.amount > 5:
        return make_response(409, data={"message": f"Dosiahli ste maximálny počet možných rezervácii pre tento spoj. Stav: ({my_seats}+{body.amount})/5"})
    
    # Get number of reserved seats
    seats = session.query(func.sum(Seat.amount)) \
                .filter(Seat.time_id == body.route) \
                .filter(Seat.date == body.date) \
                .filter(Seat.from_stop_id < body.to_stop) \
                .filter(body.from_stop < Seat.to_stop_id) \
                .first()

    # Maximum capacity reached
    seats = seats[0] if seats[0] != None else 0
    if seats + body.amount > time.vehicle.capacity:
        return make_response(409, data={"message": f"Rezervácie pre tento spoj boli vypredané. Stav: ({seats}+{body.amount})/{time.vehicle.capacity}"})

    stops: List[RouteStop] = RouteStop.query \
        .filter(RouteStop.route_id == time.route_id) \
        .filter(RouteStop.id <= body.to_stop) \
        .filter(body.from_stop <= RouteStop.id) \
        .all()

    if len(stops) < 2 or stops[0].id != body.from_stop or stops[-1].id != body.to_stop:
        return make_response(409)

    user = current_user.id if current_user.is_authenticated else None

    seat: Seat = Seat(date=body.date, amount=body.amount, price=(len(stops) - 1) * route.price, name=body.name, email=body.email, user_id=user,
        from_stop_id=body.from_stop, to_stop_id=body.to_stop, time_id=body.route, route_id=route.id)

    session.add(seat)
    session.commit()

    return make_response(200)

@bp.route("/get_seats", methods=["GET"])
@authorization([UserType.admin, UserType.staff])
def get_seats():
    seats = []
    if current_user.type == UserType.staff:
        staff: Staff = get_staff_instance(current_user.id)

        if staff == None:
            return make_response(401)

        seats = Seat.query.join(RouteTime).join(Route).filter(Route.carrier_id == staff.carrier_id).all()
    elif current_user.type == UserType.admin:
        seats = Seat.query.all()

    return make_response(200, {
        "seats": [{
            "id": seat.id,
            "date": str(seat.date),
            "amount": seat.amount,
            "price": seat.price * seat.amount,
            "paid": seat.paid,
            "name": seat.name,
            "created_at": seat.created_at,
            "email": seat.email,
            "user": {
                "id": seat.user.id,
                "username": seat.user.username,
                "name": seat.user.name,
                "email": seat.user.email,
                "type": seat.user.type
            } if seat.user != None else None,
            "from_station": {
                "id": seat.from_stop.station.id,
                "name": seat.from_stop.station.name,
                "location": seat.from_stop.station.location
            } if seat.from_stop != None else None,
            "to_station": {
                "id": seat.to_stop.station.id,
                "name": seat.to_stop.station.name,
                "location": seat.to_stop.station.location
            } if seat.to_stop != None else None,
            "route": {
                "id": seat.time.id,
                "time": str(seat.time.time),
                "info": {
                    "name": seat.route.name
                } if seat.route != None else None
            } if seat.time != None else None
        } for seat in seats]
    })

@bp.route("/get_my_seats", methods=["GET"])
@authorization([UserType.admin, UserType.passenger])
def get_my_seats():
    seats: List[Station] = Seat.query.filter(Seat.user_id == current_user.id).all()

    return make_response(200, {
        "seats": [{
            "id": seat.id,
            "date": str(seat.date),
            "amount": seat.amount,
            "price": seat.price * seat.amount,
            "paid": seat.paid,
            "name": seat.name,
            "created_at": seat.created_at,
            "email": seat.email,
            "from_station": {
                "id": seat.from_stop.station.id,
                "name": seat.from_stop.station.name,
                "location": seat.from_stop.station.location
            } if seat.from_stop != None else None,
            "to_station": {
                "id": seat.to_stop.station.id,
                "name": seat.to_stop.station.name,
                "location": seat.to_stop.station.location
            } if seat.to_stop != None else None,
            "route": {
                "id": seat.time.id,
                "time": str(seat.time.time),
                "vehicle": {
                    "name": seat.time.vehicle.name,
                    "location": f"{seat.time.vehicle.station.location} - {seat.time.vehicle.station.name}" if seat.time.vehicle.station != None else None,
                    "carrier": seat.time.vehicle.carrier.name
                } if seat.time.vehicle != None else None
            } if seat.time != None else None
        } for seat in seats] 
    })

@bp.route("/set_seat_paid/<id>", methods=["POST"])
@authorization([UserType.admin, UserType.staff])
def set_seat_paid(id: int):
    seat: Seat = Seat.query.get(id)

    if seat == None:
        return make_response(404)

    # Carrier can only update seats for its own routes
    if current_user.type == UserType.staff:
        staff: Staff = get_staff_instance(current_user.id)

        if staff == None:
            return make_response(401)

        route: Route = Route.query.get(seat.time.route_id)

        if route == None or route.carrier_id != staff.carrier_id:
            return make_response(409)

    seat.paid = True
    session.commit()

    return make_response(200)

@bp.route("/delete_seat/<id>", methods=["POST"])
@authorization([UserType.admin, UserType.staff])
def delete_seat(id: int):
    seat: Seat = Seat.query.get(id)

    if seat == None:
        return make_response(404)

    # Carrier can only delete seats for its own routes
    if current_user.type == UserType.staff:
        staff: Staff = get_staff_instance(current_user.id)

        if staff == None:
            return make_response(401)

        route: Route = Route.query.get(seat.time.route_id)

        if route == None or route.carrier_id != staff.carrier_id:
            return make_response(409)

    session.delete(seat)
    session.commit()
    
    return make_response(200)

@bp.route("/get", methods=["POST"])
@validate()
def get(body: FindForm):
    from_station: Station = get_station(body.from_station)
    to_station: Station = get_station(body.to_station)

    if from_station == None or to_station == None:
        return make_response(404, data={"message": "Musíte si vybrať z/do stanicu"})

    timestamp = datetime.combine(body.date, body.time)

    # Get all routes that have origin station in it
    query = session.query(Route.id, Route.name, Route.price, Vehicle.name, Vehicle.capacity, User.name, RouteTime.id,
        (body.date + RouteTime.time + cast(func.concat(RouteStop.departure, ' minutes'), Interval)).label("departure_time"),
        RouteStop.id)
    query = query.join(RouteTime, RouteTime.route_id == Route.id)
    query = query.join(RouteStop, RouteStop.route_id == Route.id)
    query = query.join(User, Route.carrier_id == User.id)
    query = query.join(Vehicle, RouteTime.vehicle_id == Vehicle.id)

    query = query.filter(RouteTime.repeat[func.extract("dow", body.date + RouteTime.time)] == True)
    query = query.filter(RouteStop.station_id == body.from_station)
    query = query.filter(body.date + RouteTime.time + cast(func.concat(RouteStop.departure, ' minutes'), Interval) > timestamp)
    query = query.filter(body.date + RouteTime.time + cast(func.concat(RouteStop.departure, ' minutes'), Interval) < timestamp + timedelta(minutes=60))
    query = query.order_by(text("departure_time"))

    # Get all stops of the routes
    routes = []
    for route in query.all():
        schedule = session.query(RouteStop.id, Station.id, Station.name, Station.location,
            body.date + RouteTime.time + cast(func.concat(RouteStop.arrival, ' minutes'), Interval),
            body.date + RouteTime.time + cast(func.concat(RouteStop.departure, ' minutes'), Interval))
        
        schedule = schedule.join(Route, Route.id == RouteStop.route_id)
        schedule = schedule.join(RouteTime, RouteTime.route_id == Route.id)
        schedule = schedule.join(Station, RouteStop.station_id == Station.id)
        schedule = schedule.filter(RouteTime.id == route[6])
        schedule = schedule.filter(RouteStop.id >= route[8])
        schedule = schedule.order_by(RouteStop.id)

        # Cut all the stops after target stop
        items = []
        for item in schedule.all():
            items.append(item)

            if item[1] == body.to_station:
                break

        # If the last stop is not the target one, ignore
        if len(items) < 2 or items[-1][1] != body.to_station:
            continue

        stops = []

        for stop in items:            
            stops.append({
                "id": stop[0],
                "station": {
                    "name": stop[2],
                    "location": stop[3]
                },
                "arrival": stop[4].strftime("%H:%M:%S"),
                "departure": stop[5].strftime("%H:%M:%S")
            })

        seats = session.query(func.sum(Seat.amount)) \
                    .filter(Seat.time_id == route[6]) \
                    .filter(Seat.date == body.date) \
                    .filter(Seat.from_stop_id < items[-1][0]) \
                    .filter(items[0][0] < Seat.to_stop_id) \
                    .first()

        routes.append({
            "id": route[6],
            "carrier": route[5],
            "name": route[1],
            "vehicle": {
                "name": route[3],
                "seats": seats[0] if seats[0] != None else 0,
                "capacity": route[4]
            },
            "price": (len(stops) - 1) * route[2],
            "stops": stops
        })

    return make_response(200, data={
        "routes": routes
    })