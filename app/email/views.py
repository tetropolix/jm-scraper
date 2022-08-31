from app.auth.models import User
from app.common.custom_responses import StatusCodeResponse
from app.common.decorators import register_route
from app.email.db_actions import confirm_user
from app.email.email_utils import confirm_token, send_confirmation_email
from app.email.schemas.request_schemas import ResendRequest
from app.email.schemas.response_schemas import ConfirmationResponse
from . import email_bp
from flask import request
from sqlalchemy.orm.exc import MultipleResultsFound
from pydantic import ValidationError


@register_route(
    email_bp, "/confirm", request=None, response=ConfirmationResponse, methods=["GET"]
)
def confirm():
    "URI for account confirmation, query parameter ?token=<str> must be passed in order to validate token"
    token = request.args.get("token")
    email = confirm_token(token)
    if token is None:
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
    "/resend",
    request=ResendRequest,
    response=None,
    methods=["POST"],
)
def resend():
    args = request.get_json()
    try:
        resend_req = ResendRequest(**args)
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
