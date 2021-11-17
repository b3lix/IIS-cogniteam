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

def create_user(username: str, password: str, type: UserType) -> bool:
    """Add user to database

    :param username:    Username
    :param password:    Password
    :param type:        Type of user

    :return:            True if user was created, False otherwise
    """
    user: User = User.query.filter_by(username = username).first()

    # Check if user with same username already exists
    if user is not None:
        return False

    user = User(username=username, password=generate_password_hash(password), type=type)
    session.add(user)
    session.commit()
    return True

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
