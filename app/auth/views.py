from crypt import methods
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, MultipleResultsFound
from app import auth
from app.auth import auth_bp
from flask_login import login_required
from flask import request, session
from app.auth.db_actions import (
    create_user_with_profile,
    is_email_in_use,
    load_user,
)  # load_user import is used for registering user_loader callback required by flask_login
from flask_login import login_user, logout_user
from app.auth.models import User
from app.auth.auth_utils import is_safe_url, valid_email
from .schemas.response_schemas import (
    CheckEmailResponse,
    LoginLogoutResponse,
    RegisterResponse,
    UnauthorizedResponse,
)
from app.extensions import login_manager
from .schemas.request_schemas import CheckEmailRequest, LoginRequest, RegisterRequest
from app.common.custom_responses import StatusCodeResponse
from app.common.decorators import register_route
from app.auth.schemas.common import User as UserSchema


@register_route(
    None,
    "*unauthorized*",
    request=None,
    response=UnauthorizedResponse,
    methods=[],
)
@login_manager.unauthorized_handler
def unauthorized():
    """Response for handled unauthorized access via user login"""
    return UnauthorizedResponse(**{"next": request.url_rule.rule}).dict(), 401


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


@auth_bp.route("/logout", methods=["GET"])
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


@register_route(
    auth_bp,
    "/isEmailUsed",
    request=CheckEmailRequest,
    response=CheckEmailResponse,
    methods=["POST"],
)
def is_email_used():
    """Endpoint for checking if provided email is already in use"""
    args = request.get_json()
    try:
        req = CheckEmailRequest(**args)
    except ValidationError:
        return StatusCodeResponse(400)
    try:
        return CheckEmailResponse(**{"isUsed": is_email_in_use(req.email)}).dict(), 200
    except MultipleResultsFound:
        return StatusCodeResponse(500)


@auth_bp.after_request
def print_after_session(response):
    print("user id in session AFTER REQUEST", session.get("_user_id"))
    return response


@auth_bp.route("/test", methods=["GET"])
@login_required
def test():
    return {"you must be logged in": True}
