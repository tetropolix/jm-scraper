from flask import request

from flask_login import current_user, login_required
from pydantic import ValidationError
from app.common.custom_responses import StatusCodeResponse
from app.common.decorators import register_route
from app.profile.profile_utils import createProductResponse
from app.profile import profile_bp
from app.profile.db_actions import (
    add_products_for_profile,
    remove_products_from_profile,
    verify_max_products_per_profile,
)
from app.profile.schemas.request_schemas import ProductRequest
from app.profile.schemas.response_schemas import ProductResponse


@register_route(
    profile_bp,
    "/addProduct",
    request=ProductRequest,
    response=ProductResponse,
    methods=["POST"],
)
@login_required
def add_product():
    """Add products to currently logged user profile by their ids"""
    args = request.get_json()
    try:
        product_req = ProductRequest(**args)
    except ValidationError:
        return StatusCodeResponse(400)
    # Check for maximum products per profile
    add_products = verify_max_products_per_profile(product_req, current_user)
    if not add_products:
        return StatusCodeResponse(400, "EXCEEDED MAXIMUM PRODUCTS PER PROFILE")
    added_product_ids = add_products_for_profile(product_req, current_user)
    added = True if len(added_product_ids) > 0 else 0
    return createProductResponse(added_product_ids, added), 200


@register_route(
    profile_bp,
    "/removeProduct",
    request=ProductRequest,
    response=ProductResponse,
    methods=["POST"],
)
@login_required
def remove_product():
    """Remove products from currently logged user profile by their ids"""
    args = request.get_json()
    try:
        args = ProductRequest(**args)
    except ValidationError:
        return StatusCodeResponse(400)
    removed_product_ids = remove_products_from_profile(args, current_user)
    removed = True if len(removed_product_ids) > 0 else 0
    return createProductResponse(removed_product_ids, removed=removed)
