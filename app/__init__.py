from app.config import config
from flask import Flask
from app.errorHandlers import notFound
from .extensions import login_manager, db, migrate, cors
import app.database  # register all models for migration


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
    from app.profile import profile_bp

    app.register_blueprint(products_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)

    # Errorhandlers
    app.errorhandler(404)(notFound)

    # CORS
    cors.init_app(app)

    # Auth
    login_manager.init_app(app)

    # Database
    db.init_app(app)

    # Migrate
    migrate.init_app(app, db)
    return app
