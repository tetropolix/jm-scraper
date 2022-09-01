from app.auth.models import User
from app.common.custom_responses import StatusCodeResponse
from app.common.decorators import register_route
from app.common.utils import get_request_obj
from app.email.db_actions import (
    assign_user_password_reset_token,
    confirm_user,
    reset_user_password,
)
from app.email.email_utils import (
    confirm_token,
    send_confirmation_email,
    send_password_reset_email,
)
from app.email.schemas.request_schemas import (
    ConfirmationRequest,
    PassResetRequest,
    TokenRequest,
)
from app.email.schemas.response_schemas import (
    ConfirmationResponse,
    PasswordResetResponse,
)
from . import email_bp
from flask import request
from sqlalchemy.orm.exc import MultipleResultsFound
from pydantic import ValidationError


@register_route(
    email_bp,
    "/confirm",
    request=ConfirmationRequest,
    response=ConfirmationResponse,
    methods=["POST"],
)
def confirm():
    "URI for account confirmation, token must be passed via json body"
    req = get_request_obj(request, ConfirmationRequest)
    email = confirm_token(req.token)
    if req.token is None:
        return StatusCodeResponse(400)
    elif email is None:
        return ConfirmationResponse(invalid_token=True).dict(), 200
    try:
        user = User.query_by_email(email)
    except MultipleResultsFound:
        return StatusCodeResponse(500)
    if user is None:
        return StatusCodeResponse(400)
    if user.confirmed:
        return ConfirmationResponse(already_confirmed=True).dict(), 200
    confirm_user(user)
    return ConfirmationResponse(confirmed=True).dict(), 200


@register_route(
    email_bp,
    "/passResetToken",
    request=TokenRequest,
    response=None,
    methods=["POST"],
)
def password_reset_token():
    """Method used for generating password reset token for specified user by email"""
    req = get_request_obj(request, TokenRequest)
    try:
        user = User.query_by_email(req.email)
    except MultipleResultsFound:
        return StatusCodeResponse(500)
    if user is None:
        return StatusCodeResponse(400)
    token = send_password_reset_email(req.email)
    user.password_reset_token = assign_user_password_reset_token(user, token)
    return {}, 200


@register_route(
    email_bp,
    "/passReset",
    request=PassResetRequest,
    response=PasswordResetResponse,
    methods=["POST"],
)
def password_reset():
    "Password reset for account specified by email"
    req = get_request_obj(request, PassResetRequest)
    email = confirm_token(req.token, "pass_reset")
    if (
        email != req.email
    ):  # client tries to reset password for account whose email doesnt match token email
        return StatusCodeResponse(400)
    if email is None:
        return PasswordResetResponse(invalid_token=True).dict(), 200
    try:
        user = User.query_by_email(email)
    except MultipleResultsFound:
        return StatusCodeResponse(500)
    if user is None:
        return StatusCodeResponse(400)
    if user.password_reset_token != req.token:
        return PasswordResetResponse(invalid_token=True).dict(), 200
    reset_user_password(user, req.new_password)
    return PasswordResetResponse(successful_reset=True).dict(), 200


@register_route(
    email_bp,
    "/resend",
    request=TokenRequest,
    response=None,
    methods=["POST"],
)
def resend():
    """Method used to resend confirmation token to users email address"""
    args = request.get_json()
    try:
        resend_req = TokenRequest(**args)
    except ValidationError:
        return StatusCodeResponse(400)
    try:
        user = User.query_by_email(resend_req.email)
    except MultipleResultsFound:
        return StatusCodeResponse(500)
    if user is None:
        return StatusCodeResponse(400)
    send_confirmation_email(resend_req.email)
    return {}, 200
