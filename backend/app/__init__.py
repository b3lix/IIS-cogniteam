# Standard library imports
from datetime import timedelta

# Flask related imports
from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager

# SQLalchemy related imports
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# App related imports
from config import DATABASE_URI, SECRET_KEY

from app.entities import Base
from app.entities.user import User

# Initialize SQLalchemy engine
engine = create_engine(DATABASE_URI, convert_unicode = True, pool_size=20, max_overflow=0)

# Create SQLalchemy session
session = scoped_session(sessionmaker(autocommit = False, autoflush = False, bind = engine))

# Setup query on entities
Base.query = session.query_property()
Base.metadata.create_all(bind=engine)

def make_response(status: int, data: object = ""):
    """Create flask response object

    :param status:  HTTP response status code
    :param data:    HTTP body data
    :return:        Flask response object
    """
    return (data, status)

def create_app():
    """Create flask application

    :return: Flask application object
    """
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=10)
    app.config["SESSION_REFRESH_EACH_REQUEST"] = True

    @app.after_request 
    def after_request_callback(response):
        session.close()
        return response

    # Setup CORS
    CORS(app, supports_credentials=True)

    # Setup flask login manager
    login_manager = LoginManager()
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    login_manager.init_app(app)

    # Register route blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.users import bp as users_bp
    app.register_blueprint(users_bp, url_prefix="/users")

    from app.vehicles import bp as vehicles_bp
    app.register_blueprint(vehicles_bp, url_prefix="/vehicles")

    from app.stations import bp as stations_bp
    app.register_blueprint(stations_bp, url_prefix="/stations")

    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp, url_prefix="/routes")

    from app.browser import bp as browser_bp
    app.register_blueprint(browser_bp, url_prefix="/browser")

    return app