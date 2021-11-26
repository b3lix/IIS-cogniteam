# Standard library imports
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash

# Flask related imports
from flask_login import login_required, current_user
from flask_pydantic.core import validate

# Pydantic related imports
from pydantic import BaseModel, constr, conint
from pydantic.networks import EmailStr

# App related imports
from app import make_response, session
from app.users import bp
from app.auth.model import authorization, create_user
from app.users.model import get_users, get_user, delete_user, create_staff, get_staff_record, get_staff, get_staff_instance
from app.entities.user import User, Staff, UserType

class CreateForm(BaseModel):
    username: constr(strip_whitespace=True, min_length=3)
    password: constr(strip_whitespace=True, min_length=3)
    name: constr(strip_whitespace=True, min_length=3)
    email: EmailStr
    carrier: Optional[conint(ge=0)]
    type: UserType

class UpdateForm(BaseModel):
    username: constr(strip_whitespace=True, min_length=3)
    password: Optional[constr(strip_whitespace=True, min_length=3)]
    name: constr(strip_whitespace=True, min_length=3)
    email: EmailStr
    carrier: Optional[conint(ge=0)]
    type: UserType

@bp.route("/info", methods=["GET"])
@login_required
def info():
    return make_response(200, data={
        "username": current_user.username,
        "type": int(current_user.type),
        "email": current_user.email,
        "name": current_user.name
    })

@bp.route("/create", methods=["POST"])
@authorization([UserType.admin, UserType.carrier])
@validate()
def create(body: CreateForm):
    if current_user.type == UserType.carrier:
        user: User = get_user(current_user.id)

        if user == None or user.type != UserType.carrier:
            return make_response(409)

        # Carrier can create staff only under him
        if current_user.type == UserType.carrier:
            body.carrier = current_user.id

        created: User = create_user(body.username, body.password, UserType.staff, body.email, body.username)

        if created == None:
            return make_response(409)

        create_staff(created.id, current_user.id)
        return make_response(200)

    if current_user.type == UserType.admin:
        if body.type == UserType.staff:
            carrier: User = get_user(body.carrier)
            if carrier == None or carrier.type != UserType.carrier:
                return make_response(409)

        created: bool = create_user(body.username, body.password, body.type, body.email, body.username)

        if not created:
            return make_response(409)

        if body.type == UserType.staff:
            create_staff(created.id, body.carrier)

        return make_response(200)
    
    return make_response(401)

@bp.route("/delete/<id>", methods=["POST"])
@authorization([UserType.admin, UserType.carrier])
def delete(id: int):
    user: User = get_user(id)

    if user == None:
        return make_response(404)

    if current_user.type == UserType.carrier:
        staff: Staff = get_staff_record(user.id, current_user.id)

        # Carrier can only delete own staff accounts
        if staff == None:
            return make_response(401)

    if user.type == UserType.carrier:
        for user in get_staff(user.id):
            session.delete(user)
        session.commit()

    delete_user(id)

    return make_response(200)

@bp.route("/update/<id>", methods=["POST"])
@authorization([UserType.admin, UserType.carrier])
@validate()
def update(id: int, body: UpdateForm):
    user: User = get_user(id)

    if user == None:
        return make_response(404)

    if current_user.type == UserType.carrier:
        staff: Staff = get_staff_record(user.id, current_user.id)

        # Carrier can only update own staff accounts
        if staff == None:
            return make_response(401)
    
    # Type of staff and carrier accounts cant be changed
    if (user.type == UserType.carrier and body.type != UserType.carrier) or (user.type == UserType.staff and body.type != UserType.staff):
        return make_response(409)

    user.username = body.username
    user.email = body.email
    user.name = body.name

    if current_user.type == UserType.admin:
        # Possibly changing carrier
        if body.type == UserType.staff:
            carrier: User = get_user(body.carrier)
            if carrier == None or carrier.type != UserType.carrier:
                return make_response(409)

            staff: Staff = get_staff_instance(user.id)

            if staff == None:
                create_staff(user.id, carrier.id)
            else:
                staff.carrier_id = carrier.id
                session.commit()
        
    user.type = body.type

    if body.password and body.password.strip():
        user.password = generate_password_hash(body.password)

    session.commit()
    return make_response(200)

@bp.route("/get/<id>", methods=["GET"])
@authorization([UserType.admin, UserType.carrier])
def get_one(id: int):
    user: User = get_user(id)

    if user == None:
        return make_response(404)

    # Carrier can fetch only own staff
    if current_user.type == UserType.carrier:
        staff: Staff = get_staff_record(user.id, current_user.id)

        # Carrier can only update own staff accounts
        if staff == None:
            return make_response(401)

    data = {
        "id": user.id,
        "username": user.username,
        "name": user.name,
        "email": user.email,
        "type": user.type
    }

    staff: Staff = get_staff_instance(id)

    if staff != None:
        data["carrier"] = staff.carrier_id

    return make_response(200, data=data)

@bp.route("/get", methods=["GET"])
@authorization([UserType.admin, UserType.carrier])
def get_all():
    return make_response(200, {
        "users": [{
            "id": user.id,
            "username": user.username,
            "name": user.name,
            "email": user.email,
            "type": user.type
        } for user in (get_users() if current_user.type == UserType.admin else get_staff(current_user.id))] 
    })