from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    CONFIRMATION_SALT = os.environ.get("CONFIRMATION_SALT")
    PASSRESET_SALT = os.environ.get("PASSRESET_SALT")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = os.environ.get("SESSION_TYPE")
    PERMANENT_SESSION_LIFETIME = int(os.environ.get("PERMANENT_SESSION_LIFETIME"))
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")


class DevelopmentLocalConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI_DEV_LOCAL")
    SHOW_DOCS = True
    SESSION_COOKIE_SAMESITE = os.environ.get("SESSION_COOKIE_SAMESITE")
    SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE")


class DevelopmentRemoteConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI_DEV_REMOTE")
    SHOW_DOCS = True
    SESSION_COOKIE_SAMESITE = os.environ.get("SESSION_COOKIE_SAMESITE")
    SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE")
    SESSION_COOKIE_DOMAIN = os.environ.get("SESSION_COOKIE_DOMAIN")


config = {
    "developmentLocal": DevelopmentLocalConfig,
    "developmentRemote": DevelopmentRemoteConfig,
}
