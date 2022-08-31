from typing import List, Optional, Union
from flask import current_app
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from app.extensions import mail
from flask import url_for

CONFIRMATION_EMAIL_SUBJECT = "New user account confirmation"
CONFIRMATION_EMAIL_BODY = """Welcome, please use the following link for activating your account

{}

Activation link is valid for 60 minutes.
This email is automatically generated, please do not respond."""


def generate_confirmation_token(email: str):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return serializer.dumps(email, salt=current_app.config["CONFIRMATION_SALT"])


def confirm_token(token, expiration=3600) -> Optional[str]:
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        email = serializer.loads(
            token, salt=current_app.config["CONFIRMATION_SALT"], max_age=expiration
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


def send_confirmation_email(user_email: str):
    token = generate_confirmation_token(user_email)
    confirm_url = url_for("email_bp.confirm", token=token, _external=True)
    send_email(
        user_email,
        CONFIRMATION_EMAIL_SUBJECT,
        body=CONFIRMATION_EMAIL_BODY.format(confirm_url),
    )
