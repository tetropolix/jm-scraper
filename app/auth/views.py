from sqlalchemy.exc import IntegrityError
from app.auth import auth_bp
from flask_login import login_required
from flask import render_template, request, session

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email
from app.auth.db_actions import (
    create_user_with_profile,
)  # load_user import is used for registering user_loader callback required by flask_login
from flask_login import login_user, logout_user
from app.auth.models import User
from app.auth.schemas import (
    RegisterReponse,
    User as UserSchema,
    LoginLogoutResponse,
)
from app.auth.auth_utils import is_safe_url
from app.common.custom_responses import StatusCodeResponse


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Keep me logged in")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "GET":
        next = request.args.get("next")
        return render_template("login_form.html", form=form, next=next)
    else:
        email = request.json.get("email")
        password = request.json.get("password")
        next = (
            None if request.args.get("next") in (None, "") else request.args.get("next")
        )
        if not email or not password:
            return StatusCodeResponse(400)
        user = User.query_by_email(email)
        if user is not None and user.verify_password(password):
            logged = login_user(user)
            if not logged:
                return (
                    LoginLogoutResponse(
                        logged=False, error="Unable to log in user", user=None
                    ).json(),
                    500,
                )
            userSchemaObj = UserSchema(email=user.email, username=user.username)
            if next is None:
                return LoginLogoutResponse(logged=True, user=userSchemaObj).json(), 200
            elif next and is_safe_url(next):
                return (
                    LoginLogoutResponse(
                        logged=True, user=userSchemaObj, next=next
                    ).json(),
                    200,
                )
            elif next and not is_safe_url(next):
                return StatusCodeResponse(400)
        return LoginLogoutResponse(error="User not found or wrong password").json(), 200


@auth_bp.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return LoginLogoutResponse(logged=False, error=None, user=None).json(), 200


@auth_bp.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")
    user = User.query_by_email(email)
    if user is not None:
        response = RegisterReponse(error="Specified email is already in use")
        return response.json(), 200
    else:
        try:
            newUser = User(email=email, username=username, password=password)
            create_user_with_profile(newUser)
            userSchemaObj = UserSchema(email=email, username=username)
            response = RegisterReponse(registered=True, user=userSchemaObj)
            return response.json(), 200
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
