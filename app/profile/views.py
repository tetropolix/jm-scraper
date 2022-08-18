from flask import request

from flask_login import current_user, login_required
from psycopg2 import IntegrityError
from pydantic import ValidationError
from app.common.custom_responses import StatusCodeResponse
from app.common.decorators import register_route
from app.common.utils import create_product_without_product_data
from ..common.exceptions import NotValidUrlPathError
from .models import Profile
from app.profile.profile_utils import get_user_profile_dict
from app.profile import profile_bp
from app.profile.db_actions import (
    update_products_for_profile,
    update_user_profile_personal_info,
    update_user_profile_predefined_filters,
    verify_max_products_per_profile,
)
from app.profile.schemas.request_schemas import (
    UserProfileRequest,
    UserProfileProductsRequest,
)
from app.profile.schemas.response_schemas import (
    UserProfileProductsResponse,
    UserProfileResponse,
)


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
    request=UserProfileRequest,
    response=UserProfileResponse,
    methods=["POST"],
)
@login_required
def update_user_profile():
    """Updates profile info for currently logged in user - do not work for profile products"""
    args = request.get_json()
    try:
        req = UserProfileRequest(**args)
    except ValidationError:
        return StatusCodeResponse(400)
    if req.number_of_sections_to_update() != 1 or req.product_ids is not None:
        return StatusCodeResponse(400)
    # Update profile
    try:
        if req.should_update_personal_info():
            updated_profile: Profile = update_user_profile_personal_info(
                req, current_user
            )
        elif req.should_update_filters():
            updated_profile: Profile = update_user_profile_predefined_filters(
                req, current_user
            )
        else:
            return StatusCodeResponse(400)
        updated_profile_dict = updated_profile.get_profile_dict()
        return UserProfileResponse(**updated_profile_dict).dict(), 200
    except NotValidUrlPathError:
        return StatusCodeResponse(400)
    except IntegrityError:
        return StatusCodeResponse(500)
    except ValidationError:
        return StatusCodeResponse(
            500, "INTERNAL SERVER ERROR - Unable to construct response"
        )


@register_route(
    profile_bp,
    "/updateUserProfileProducts",
    request=UserProfileProductsRequest,
    response=UserProfileProductsResponse,
    methods=["POST"],
)
@login_required
def update_user_profile_products():
    """Update (add or remove) products from profile by their id/ids"""
    args = request.get_json()
    try:
        product_req = UserProfileProductsRequest(**args)
    except ValidationError:
        return StatusCodeResponse(400)
    # Check for maximum products per profile
    add_products = verify_max_products_per_profile(product_req, current_user)
    if not add_products:
        return StatusCodeResponse(400, "EXCEEDED MAXIMUM PRODUCTS PER PROFILE")
    try:
        (
            updated_products_list,
            number_of_affected_products,
            max_products,
        ) = update_products_for_profile(product_req, current_user)
    except IntegrityError:
        return StatusCodeResponse(500)
    return (
        UserProfileProductsResponse(
            **{
                "maxProductsForProfile": max_products,
                "numberOfAffectedProducts": number_of_affected_products,
                "products": [
                    create_product_without_product_data(prod, create_dict=True)
                    for prod in updated_products_list
                ],
            }
        ).dict(),
        200,
    )
