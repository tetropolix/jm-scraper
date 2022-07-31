from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentLocalConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI_DEV")


class DevelopmentRemoteConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABSE_URL")


config = {
    "developmentLocal": DevelopmentLocalConfig,
    "developmentRemote": DevelopmentRemoteConfig,
}
