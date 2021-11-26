# Flask related imports
from flask import request
from flask_login.utils import logout_user
from flask_pydantic import validate
from flask_login import login_user, login_required, current_user

# Pydantic related imports
from pydantic import BaseModel, constr
from pydantic.networks import EmailStr

# App related imports
from app import make_response
from app.auth import bp
from app.auth.model import authenticate, authorization, create_user

from app.entities.user import User, UserType

class RegisterForm(BaseModel):
    username: constr(strip_whitespace=True, min_length=3)
    password: constr(strip_whitespace=True, min_length=3)
    name: constr(strip_whitespace=True, min_length=3)
    email: EmailStr

class LoginForm(BaseModel):
    username: constr(strip_whitespace=True, min_length=3)
    password: constr(strip_whitespace=True, min_length=3)

@bp.route("/register", methods=["POST"])
@validate()
def register(body: RegisterForm):
    created: User = create_user(body.username, body.password, UserType.passenger, body.email, body.name)

    if created == None:
        return make_response(409, data={"message": "Uživateľ s týmto prihlasovacím menom alebo emailom už existuje"})

    return make_response(200)

@bp.route("/login", methods=["POST"])
@validate()
def login(body: LoginForm):
    user: User = authenticate(body.username, body.password)
    
    if user == None:
        return make_response(401, data={"message": "Zadané prihlasovacie údaje sú nesprávne"})

    login_user(user)
    return make_response(200)

@bp.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return make_response(200)
