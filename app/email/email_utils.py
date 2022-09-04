from typing import List, Literal, Optional, Union
from flask import current_app
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from app.extensions import mail
from flask import url_for

FRONTEND_BASE = current_app.config["FRONTEND_BASE"]

CONFIRMATION_EMAIL_SUBJECT = "New user account confirmation"
CONFIRMATION_EMAIL_BODY = """Welcome, please use the following link for activating your account

{}

Activation link is valid for 60 minutes.
This email is automatically generated, please do not respond."""

PASS_RESET_EMAIL_SUBJECT = "Password reset for your account"
PASS_RESET_EMAIL_BODY = """Please use the following link for resetting your password

{}

Link is valid for 60 minutes.
This email is automatically generated, please do not respond."""


def get_token_salt(type: str) -> str:
    salts = {"confirmation": "CONFIRMATION_SALT", "pass_reset": "PASSRESET_SALT"}
    return current_app.config[salts[type]]


def generate_token(email: str, token_type: Literal["confirmation", "pass_reset"]):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return serializer.dumps(email, salt=get_token_salt(token_type))


def confirm_token(
    token, token_type: Literal["confirmation", "pass_reset"], expiration=3600
) -> Optional[str]:
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        email = serializer.loads(
            token, salt=get_token_salt(token_type), max_age=expiration
        )
    except:
        return None
    return email


def send_email(
    to: Union[str, List[str]], subject: str, body: str = None, html_template: str = None
):
    if not body and not html_template:
        raise ValueError("Email must contain body or html template")
    recipients = to if isinstance(to, list) else [to]
    msg = Message(
        recipients=recipients,
        subject=subject,
    )
    if body is not None:
        msg.body = body
    if html_template is not None:
        msg.html = html_template
    mail.send(msg)


def send_confirmation_email(user_email: str) -> str:
    """Sends confirmation email with token, returns generated token"""
    token = generate_token(user_email, "confirmation")
    confirm_url = url_for(FRONTEND_BASE + "/confirm", token=token, _external=True)
    send_email(
        user_email,
        CONFIRMATION_EMAIL_SUBJECT,
        body=CONFIRMATION_EMAIL_BODY.format(confirm_url),
    )
    return token


def send_password_reset_email(user_email: str) -> str:
    """Sends password reset email with token, returns generated token"""
    token = generate_token(user_email, "pass_reset")
    confirm_url = url_for(FRONTEND_BASE + "/passReset", token=token, _external=True)
    send_email(
        user_email,
        PASS_RESET_EMAIL_SUBJECT,
        body=PASS_RESET_EMAIL_BODY.format(confirm_url),
    )
    return token
