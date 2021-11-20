# Flask related imports
from flask import Blueprint

bp = Blueprint("routes", __name__)

# App related imports
from app.routes import routes