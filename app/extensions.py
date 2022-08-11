from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

cors = CORS(
    resources={
        r"/products": {
            "origins": ["http://localhost:4200", "https://vagoshop.netlify.app/"],
            "methods": ["POST", "OPTIONS"],
        },
        r"/products/*": {
            "origins": ["http://localhost:4200", "https://vagoshop.netlify.app/"],
            "methods": ["POST", "OPTIONS"],
        },
    }
)
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth_bp.login"
