# Flask related imports
from flask import Blueprint

bp = Blueprint("browser", __name__)

# App related imports
from app.browser import routes