from flask import Blueprint

email_bp = Blueprint("email_bp", __name__, url_prefix="/email")

from . import views
