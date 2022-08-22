from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = int(os.environ.get("PERMANENT_SESSION_LIFETIME"))
    SESSION_COOKIE_DOMAIN = 'dev.localhost'
    SESSION_COOKIE_SAMESITE = None


class DevelopmentLocalConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI_DEV_LOCAL")
    SHOW_DOCS = True


class DevelopmentRemoteConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI_DEV_REMOTE")
    SHOW_DOCS = True
    SESSION_COOKIE_DOMAIN = 'herokuapp.com'
    SESSION_COOKIE_SAMESITE = None
    SESSION_COOKIE_SECURE = True


config = {
    "developmentLocal": DevelopmentLocalConfig,
    "developmentRemote": DevelopmentRemoteConfig,
}
