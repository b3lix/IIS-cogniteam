# Standard library imports
from typing import List
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

# Flask related imports
from flask_login import current_user
from flask_login.utils import login_required

# App related imports
from app import session, make_response
from app.entities.user import User, UserType
from app.entities.seat import Seat

def create_user(username: str, password: str, type: UserType, email: str, name: str) -> User:
    """Add user to database

    :param username:    Username
    :param password:    Password
    :param type:        Type of user

    :return:            True if user was created, False otherwise
    """
    user: User = User.query.filter_by(username = username).first()

    # Check if user with same username already exists
    if user is not None:
        return None

    user: User = User.query.filter_by(email = email).first()

    # Check if user with same email already exists
    if user is not None:
        return None

    user = User(username=username, password=generate_password_hash(password), type=type, email=email, name=name)
    session.add(user)
    session.flush()
    session.refresh(user)

    # Add all non registered reservations of this email to this account
    Seat.query.filter(Seat.email == email).filter(Seat.user_id == None).update({ Seat.user_id: user.id })

    session.commit()
    return user

def authenticate(username: str, password: str) -> User:
    """Verify user credentials

    :param username:    Username
    :param password:    Password

    :return:            True if credentials are correct, False otherwise
    """
    user: User = User.query.filter_by(username = username).first()
    if user is None or not check_password_hash(user.password, password):
        return None
    return user

def authorization(roles: List[UserType]):
    """Authorization decorator
    Verifies role of user

    :param roles:       Roles that have access to this resource
    """
    def decorator(func):
        @login_required
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.type not in roles:
                return make_response(401)

            return func(*args, **kwargs)
        return wrapper
    return decorator
