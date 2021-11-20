# Standard library imports
from typing import List

# App related imports
from app import session
from app.auth.model import create_user
from app.entities.user import User, Staff, UserType

def get_user(id: int) -> User:
    """Get user from database

    :param id:  User id
    """
    return User.query.get(id)

def delete_user(id: int) -> None:
    """Delete user from database

    :param id:  User id
    """
    session.delete(User.query.get(id))
    session.commit()

def create_staff(user_id: int, carrier_id: int) -> None:
    """Add staff to database

    :param user_id:     User ID
    :param carrier_id:    Carrier ID
    """
    staff = Staff(user_id=user_id, carrier_id=carrier_id)
    session.add(staff)
    session.commit()

def get_staff_record(user_id: int, carrier_id: int) -> Staff:
    """Check if account is staff of carrier

    :param user_id:       User ID
    :param carrier_id:    Carrier ID
    """
    return Staff.query.filter(Staff.user_id == user_id and Staff.carrier_id == carrier_id).first()

def get_users() -> List[User]:
    """Get users from database
    """
    return User.query.all()

def get_staff(carrier_id: int) -> List[User]:
    """Get staff of carrier from database
    """
    return User.query.filter(User.type == UserType.staff).join(Staff, Staff.user_id == User.id).filter(Staff.carrier_id == carrier_id).all()

def get_staff_instance(user_id: int) -> Staff:
    """Get staff from database
    """
    return Staff.query.filter(Staff.user_id == user_id).first()