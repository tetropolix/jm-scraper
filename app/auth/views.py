from datetime import datetime, timedelta
import smtplib
from typing import Optional
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, MultipleResultsFound
from app.auth import auth_bp
from flask_login import login_required, current_user
from flask import request, session, current_app, url_for
from app.auth.db_actions import auth_user, create_user_with_profile, is_email_in_use
from flask_login import login_user, logout_user
from app.auth.models import User, UserSession
from app.auth.auth_utils import is_safe_url, valid_email
from app.email.email_utils import (
    send_confirmation_email,
)
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
from app.extensions import db


@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user


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
        userSchemaObj = UserSchema(email=user.email, username=user.username)
        if user.confirmed == False:
            return (
                LoginLogoutResponse(user=userSchemaObj, needs_to_confirm=True).dict(),
                200,
            )
        logged = login_user(user)
        if not logged:
            return StatusCodeResponse(500)
        if next and not is_safe_url(next):
            return StatusCodeResponse(400)
        elif next and is_safe_url(next):  # if next is okay just pass
            pass
        auth_user(user, True)
        return (
            LoginLogoutResponse(logged=True, user=userSchemaObj, next=next).dict(),
            200,
        )
    LoginLogoutResponse().dict(), 200


@auth_bp.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logs out currently logged user"""
    user = current_user
    auth_user(user, False)
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
        newUser = User(
            email=email,
            username=username,
            password=password,
            confirmed=False,
            created_at=datetime.now(),
        )
        create_user_with_profile(newUser)
        userSchemaObj = UserSchema(email=email, username=username)
        send_confirmation_email(newUser.email)
        return RegisterResponse(registered=True, user=userSchemaObj).dict(), 200
    except (IntegrityError, smtplib.SMTPServerDisconnected):
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


# Method imported in app.__init__ as it is used globally (app.before_request)
def validate_session_for_auth_user() -> None:
    if "_user_id" not in session:
        return
    if request.endpoint == "auth_bp.logout":
        return
    user: Optional[User] = User.query.get(session["_user_id"])
    user_session: Optional[UserSession] = user.session
    now = datetime.now()
    session_lifetime = current_app.config["PERMANENT_SESSION_LIFETIME"]
    # Session stored in database has already expired or user is logged out
    if user_session.expires_at <= now or user.authenticated == False:
        user.authenticated = False
        if user_session is not None:
            db.session.delete(user_session)
    # session is still valid
    elif user_session.expires_at > now:
        user_session.expires_at = now + timedelta(seconds=session_lifetime)
    db.session.add(user)
    db.session.commit()


@auth_bp.route("/test", methods=["POST"])
def test():

    return {"you must be logged in": True}
