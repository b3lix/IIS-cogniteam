# Flask related imports
from flask import Blueprint

bp = Blueprint("vehicles", __name__)

# App related imports
from app.vehicles import routes