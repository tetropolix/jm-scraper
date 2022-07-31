from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentLocalConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI_DEV_LOCAL")


class DevelopmentRemoteConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI_DEV_REMOTE")


config = {
    "developmentLocal": DevelopmentLocalConfig,
    "developmentRemote": DevelopmentRemoteConfig,
}
