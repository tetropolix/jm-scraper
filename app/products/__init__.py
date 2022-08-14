from flask import Blueprint

products_bp = Blueprint("products_bp", __name__, url_prefix="/products")

from . import views
