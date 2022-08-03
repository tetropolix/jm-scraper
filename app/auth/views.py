from app.auth import auth_bp
from flask_login import login_required
import app.auth.db_actions
from flask import render_template, request, abort

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email
from app.auth.db_actions import queryUserByEmail


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Keep me logged in")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "GET":
        return render_template("login_form.html", form=form)
    else:
        email = request.form.get("email")
        password = request.form.get("password")
        if not email or not password:
            abort(400)
        user = queryUserByEmail(email)
        print("user", user)
    return {"login": True}


@auth_bp.route("/registerEmail")
@login_required
def register_email():
    return {}
