# Flask related imports
from flask import request
from flask_login.utils import logout_user
from flask_pydantic import validate
from flask_login import login_user, login_required

# Pydantic related imports
from pydantic import BaseModel

# App related imports
from app import make_response
from app.auth import bp
from app.auth.model import authenticate, authorization, create_user

from app.entities.user import User, UserType

class RegisterForm(BaseModel):
    username: str
    password: str

class LoginForm(BaseModel):
    username: str
    password: str

@bp.route("/register", methods=["POST"])
@validate()
def register(body: RegisterForm):
    created: bool = create_user(body.username, body.password, UserType.passenger)

    if not created:
        return make_response(409)

    return make_response(200)

@bp.route("/login", methods=["POST"])
@validate()
def login(body: LoginForm):
    user: User = authenticate(body.username, body.password)
    
    if user == None:
        return make_response(401)

    login_user(user)
    return make_response(200)

@bp.route("/logout", methods=["POST"])
def login_required():
    logout_user()
    return make_response(200)