from datetime import datetime
from app.auth.models import User
from app.extensions import db


def confirm_user(user: User):
    user.confirmed = True
    user.confirmed_on = datetime.now()
    db.session.add(user)
    db.session.commit()
