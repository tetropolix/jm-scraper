from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from app.config import config
from os import environ

ENVIRONMENT_TYPE = environ.get("ENV_TYPE")

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth_bp.login"


class ConfigNameNotFoundError(Exception):
    pass


def create_app(config_name):
    if config_name == None:
        raise ConfigNameNotFoundError("Config name was not specified - equals to None")
    configClass = config.get(config_name)
    if configClass == None:
        raise ConfigNameNotFoundError(
            config_name + " " + "was not found in this environment"
        )
    # App instance
    app = Flask(__name__)
    app.config.from_object(configClass)

    # Blueprints
    from app.products import products_bp
    from app.auth import auth_bp

    app.register_blueprint(products_bp)
    app.register_blueprint(auth_bp)

    # Auth
    login_manager.init_app(app)

    # Database
    db.init_app(app)
    return app


app = create_app(ENVIRONMENT_TYPE)
