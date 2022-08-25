from app.auth.views import validate_session_for_auth_user
from app.config import config
from flask import Flask
from app.errorHandlers import handler_400
from .extensions import (
    development_docs,
    login_manager,
    db,
    migrate,
    cors,
    sess,
)
from app.auth import models as authModels
from app.products import models as productsModels
from app.profile import models as profileModels  # register all models for migration


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

    # Development docs
    if app.config.get("SHOW_DOCS"):
        app.route("/api-docs", methods=["GET"])(development_docs(app))
    # Errorhandlers
    app.errorhandler(400)(handler_400)

    # Authentication before request
    app.before_request(validate_session_for_auth_user)

    # CORS
    cors.init_app(app)

    # Auth
    login_manager.init_app(app)

    # session
    sess.init_app(app)

    # Database
    db.init_app(app)

    # Migrate
    migrate.init_app(app, db)
    return app
