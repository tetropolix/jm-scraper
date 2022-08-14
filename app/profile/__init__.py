from flask import Blueprint

profile_bp = Blueprint("profile_bp", __name__, url_prefix="/profile")

from . import views
