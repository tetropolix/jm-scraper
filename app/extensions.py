from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_session import Session
from flask_mail import Mail
from app.common.custom_classes import DocumentedApp

cors = CORS(
    resources={
        r"/products": {
            "origins": ["http://localhost:4200", "https://vagoshop.netlify.app"],
            "methods": ["POST", "OPTIONS", "GET"],
        },
        r"/products/*": {
            "origins": ["http://localhost:4200", "https://vagoshop.netlify.app"],
            "methods": ["POST", "OPTIONS", "GET"],
        },
        r"/auth/*": {
            "origins": ["http://localhost:4200", "https://vagoshop.netlify.app"],
            "methods": ["GET", "POST", "OPTIONS"],
        },
        r"/profile/*": {
            "origins": ["http://localhost:4200", "https://vagoshop.netlify.app"],
            "methods": ["GET", "POST", "OPTIONS"],
        },
    },
    supports_credentials=True,
    allow_headers=[
        "Origin",
        "X-Requested-With",
        "Content-Type",
        "Accept",
        "access-control-allow-origin",
        "access-control-allow-headers",
    ],
)
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
sess = Session()
mail = Mail()


def development_docs(app):
    def function():

        for rule in app.url_map.iter_rules():
            if str(rule) in DocumentedApp.ENDPOINTS:
                DocumentedApp.add_additional_info_for_endpoint(
                    str(rule), methods=rule.methods
                )
        return DocumentedApp.schema()

    return function
