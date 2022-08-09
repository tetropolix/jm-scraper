from os import environ
from app import create_app

ENVIRONMENT_TYPE = environ.get("ENV_TYPE")

if __name__ == "__main__":
    app = create_app(ENVIRONMENT_TYPE)
    app.run()
