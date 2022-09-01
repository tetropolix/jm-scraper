from datetime import datetime
from app.auth.models import User
from app.extensions import db


def confirm_user(user: User):
    user.confirmed = True
    user.confirmed_on = datetime.now()
    db.session.add(user)
    db.session.commit()


def assign_user_password_reset_token(user: User, token: str):
    user.password_reset_token = token
    db.session.add(user)
    db.session.commit()


def reset_user_password(user: User, new_password: str):
    user.password = new_password
    user.password_reset_token = None
    db.session.add(user)
    db.session.commit()
