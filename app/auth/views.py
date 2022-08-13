from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from app.auth import auth_bp
from flask_login import login_required
from flask import request, session
from app.auth.db_actions import (
    create_user_with_profile,
)  # load_user import is used for registering user_loader callback required by flask_login
from flask_login import login_user, logout_user
from app.auth.models import User
from app.auth.auth_utils import is_safe_url, valid_email
from .schemas.response_schemas import LoginLogoutResponse, RegisterResponse
from .schemas.request_schemas import LoginRequest, RegisterRequest
from app.common.custom_responses import StatusCodeResponse
from app.common.decorators import register_route
from app.auth.schemas.common import User as UserSchema


@register_route(
    auth_bp,
    "/login",
    request=LoginRequest,
    response=LoginLogoutResponse,
    methods=["POST"],
)
def login():
    """Logs in user with specified credentials"""
    args = request.get_json()
    try:
        login_req = LoginRequest(**args)
    except ValidationError:
        return StatusCodeResponse(400)
    next = None if request.args.get("next") in (None, "") else request.args.get("next")
    email = login_req.email
    password = login_req.password
    if not email or not password:
        return StatusCodeResponse(400)
    user = User.query_by_email(email)
    if user is not None and user.verify_password(password):
        logged = login_user(user)
        if not logged:
            return StatusCodeResponse(500)
        userSchemaObj = UserSchema(email=user.email, username=user.username)
        if next is None:
            return LoginLogoutResponse(logged=True, user=userSchemaObj).dict(), 200
        elif next and is_safe_url(next):
            return (
                LoginLogoutResponse(logged=True, user=userSchemaObj, next=next).dict(),
                200,
            )
        elif next and not is_safe_url(next):
            return StatusCodeResponse(400)
    return LoginLogoutResponse().dict(), 200


@register_route(
    auth_bp,
    "/logout",
    request=None,
    response=LoginLogoutResponse,
    methods=["GET"],
)
@login_required
def logout():
    """Logs out currently logged user"""
    logout_user()
    return LoginLogoutResponse(logged=False, user=None).dict(), 200


@register_route(
    auth_bp,
    "/register",
    request=RegisterRequest,
    response=RegisterResponse,
    methods=["POST"],
)
def register():
    """Register new user with specified credentials"""
    args = request.get_json()
    try:
        register_req = RegisterRequest(**args)
    except ValidationError:
        return StatusCodeResponse(400)
    email = register_req.email
    username = register_req.username
    password = register_req.password
    retry_password = register_req.retryPassword
    user = User.query_by_email(email)
    if user is not None:
        return RegisterResponse(errorOnRegister="EMAIL_IN_USE").dict(), 200
    elif valid_email(email) == None:
        return RegisterResponse(errorOnRegister="INVALID_EMAIL").dict(), 200
    elif len(username) == 0:
        return RegisterResponse(errorOnRegister="EMPTY_USERNAME").dict(), 200
    elif len(password) < 8:
        return RegisterResponse(errorOnRegister="SHORT_PASSWORD").dict(), 200
    elif password != retry_password:
        return RegisterResponse(errorOnRegister="PASSWORD_NO_MATCH").dict(), 200
    try:
        newUser = User(email=email, username=username, password=password)
        create_user_with_profile(newUser)
        userSchemaObj = UserSchema(email=email, username=username)
        return RegisterResponse(registered=True, user=userSchemaObj).dict(), 200
    except IntegrityError:
        return StatusCodeResponse(500)


@auth_bp.before_request
def reload_session():
    if "_user_id" in session:
        session.modified = True


@auth_bp.route("/test", methods=["GET"])
@login_required
def test():
    return {"you must be logged in": True}
