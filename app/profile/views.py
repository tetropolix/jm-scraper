from flask import request

from flask_login import current_user, login_required
from pydantic import ValidationError
from app.common.custom_responses import StatusCodeResponse
from app.profile.profile_utils import createProductResponse
from app.profile import profile_bp
from app.profile.db_actions import (
    add_products_for_profile,
    remove_products_from_profile,
    verify_max_products_per_profile,
)
from app.profile.schemas import ProductRequest
from .profile_utils import createErrorProductResponse


@profile_bp.route("/addProduct", methods=["POST"])
@login_required
def add_product():
    # Check content type of request
    if request.content_type != "application/json":
        return StatusCodeResponse(400)
    args = request.get_json()
    # try to create valid request format from given body
    try:
        args = ProductRequest(**args)
    except ValidationError:
        return StatusCodeResponse(400)
    # Check for maximum products per profile
    add_products = verify_max_products_per_profile(args, current_user)
    if not add_products:
        return StatusCodeResponse(400, "EXCEEDED MAXIMUM PRODUCTS PER PROFILE")
    added_product_ids = add_products_for_profile(args, current_user)
    added = True if len(added_product_ids) > 0 else 0
    return createProductResponse(added_product_ids, added), 200


@profile_bp.route("/removeProduct", methods=["POST"])
@login_required
def remove_product():
    # Check content type of request
    if request.content_type != "application/json":
        return StatusCodeResponse(400)
    args = request.get_json()
    # try to create valid request format from given body
    try:
        args = ProductRequest(**args)
    except ValidationError:
        return StatusCodeResponse(400)
    removed_product_ids = remove_products_from_profile(args, current_user)
    removed = True if len(removed_product_ids) > 0 else 0
    return createProductResponse(removed_product_ids, removed=removed)
