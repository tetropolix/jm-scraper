from flask import request

from flask_login import current_user, login_required
from pydantic import ValidationError
from app.profile.profile_utils import createProductResponse
from app.profile import profile_bp
from app.profile.db_actions import (
    add_products_for_profile,
    remove_products_from_profile,
)
from app.profile.schemas import ProductRequest
from .profile_utils import createErrorProductResponse


@profile_bp.route("/addProduct", methods=["POST"])
@login_required
def add_product():
    # Check content type of request
    if request.content_type != "application/json":
        return createErrorProductResponse("Wrong content-type used"), 400
    args = request.get_json()
    # try to create valid request format from given body
    try:
        args = ProductRequest(**args)
    except ValidationError:
        return createErrorProductResponse("Wrong request body format"), 400
    added_product_ids = add_products_for_profile(args, current_user)
    added = True if len(added_product_ids) > 0 else 0
    return createProductResponse(added_product_ids, added), 200


@profile_bp.route("/removeProduct", methods=["POST"])
@login_required
def remove_product():
    # Check content type of request
    if request.content_type != "application/json":
        return createErrorProductResponse("Wrong content-type used"), 400
    args = request.get_json()
    # try to create valid request format from given body
    try:
        args = ProductRequest(**args)
    except ValidationError:
        return createErrorProductResponse("Wrong request body format"), 400
    removed_product_ids = remove_products_from_profile(args, current_user)
    removed = True if len(removed_product_ids) > 0 else 0
    return createProductResponse(removed_product_ids, removed=removed)
