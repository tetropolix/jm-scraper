from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = os.environ.get("PERMANENT_SESSION_LIFETIME")


class DevelopmentLocalConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI_DEV_LOCAL")
    PERMANENT_SESSION_LIFETIME = 600


class DevelopmentRemoteConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI_DEV_REMOTE")


config = {
    "developmentLocal": DevelopmentLocalConfig,
    "developmentRemote": DevelopmentRemoteConfig,
}
