from flask import request

from flask_login import current_user, login_required
from pydantic import ValidationError
from app.common.custom_responses import StatusCodeResponse
from app.common.decorators import register_route
from .models import Profile
from app.profile.profile_utils import createProductResponse, get_user_profile_dict
from app.profile import profile_bp
from app.profile.db_actions import (
    add_products_for_profile,
    remove_products_from_profile,
    update_user_profile_info,
    verify_max_products_per_profile,
)
from app.profile.schemas.request_schemas import ProductRequest, UpdateUserProfileRequest
from app.profile.schemas.response_schemas import ProductResponse, UserProfileResponse


@register_route(
    profile_bp,
    "/userProfile",
    request=None,
    response=UserProfileResponse,
    methods=["GET"],
)
@login_required
def get_user_profile():
    """Returns ALL profile info for currently logged in user"""
    user_profile_dict = get_user_profile_dict(current_user)
    try:
        return UserProfileResponse(**{"profile": user_profile_dict}).dict(), 200
    except ValidationError as e:
        print(e)
        return StatusCodeResponse(500)


@register_route(
    profile_bp,
    "/updateUserProfile",
    request=UpdateUserProfileRequest,
    response=UserProfileResponse,
    methods=["PUT"],
)
@login_required
def update_user_profile():
    """Updates profile info for currently logged in user"""
    args = request.get_json()
    try:
        req = UpdateUserProfileRequest(**args)
    except ValidationError:
        return StatusCodeResponse(500)
    updated_profile: Profile = update_user_profile_info(req, current_user)
    updated_profile_dict = updated_profile.get_profile_dict()
    try:
        return UserProfileResponse(**updated_profile_dict).dict(), 200
    except ValidationError:
        return StatusCodeResponse(500)


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
