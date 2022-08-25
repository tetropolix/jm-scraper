from datetime import datetime, timedelta
from flask import current_app
from app.auth.models import User, UserSession
from app.profile.models import PredefinedProfileFilters, Profile
from app.extensions import db


def create_user_with_profile(user: User) -> int:
    profile = Profile(user_id=user.id)
    profile.predefined_profile_filters = PredefinedProfileFilters(id=profile.id)
    user.profile = profile
    db.session.add(user)
    db.session.commit()
    return user.id


def is_email_in_use(email: str):
    return User.query.filter(User.email == email).scalar() is not None


def auth_user(user: User, authenticated: bool):
    user.authenticated = authenticated
    session_lifetime = current_app.config["PERMANENT_SESSION_LIFETIME"]
    if authenticated:
        expires_at = datetime.now() + timedelta(seconds=session_lifetime)
        if session_lifetime is None:
            raise ValueError("For user auth, session lifetime cannot be None")
        user_session = user.session
        if user_session == None:
            user.session = UserSession(user_id=user.id, expires_at=expires_at)
        else:
            user_session.expires_at = expires_at
    else:
        if user.session is not None:
            db.session.delete(user.session)
    db.session.add(user)
    db.session.commit()
