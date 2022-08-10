from typing import Optional
from app import login_manager
from app.auth.models import User
from app.profile.models import Profile
from app.extensions import db


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_user_with_profile(user: User) -> int:
    profile = Profile(user_id=user.id)
    user.profile = profile
    db.session.add(user)
    db.session.commit()
    return user.id
