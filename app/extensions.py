from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from app.common.general_schemas import DocumentedApp

cors = CORS(
    resources={
        r"/products": {
            "origins": ["http://localhost:4200", "https://vagoshop.netlify.app"],
            "methods": ["POST", "OPTIONS"],
        },
        r"/products/*": {
            "origins": ["http://localhost:4200", "https://vagoshop.netlify.app"],
            "methods": ["POST", "OPTIONS"],
        },
    }
)
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth_bp.login"


def development_docs(app):
    def function():

        for rule in app.url_map.iter_rules():
            if str(rule) in DocumentedApp.ENDPOINTS:
                DocumentedApp.add_additional_info_for_endpoint(
                    str(rule), methods=rule.methods
                )
        return DocumentedApp.schema()

    return function
