from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import config

db = SQLAlchemy()

def create_app(config_name):
    # App instance
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Database
    db.init_app(app)
    return app

app = create_app('development')


