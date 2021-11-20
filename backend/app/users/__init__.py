# Flask related imports
from flask import Blueprint

bp = Blueprint("users", __name__)

# App related imports
from app.users import routes