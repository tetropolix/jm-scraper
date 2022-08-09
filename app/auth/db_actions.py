from typing import Optional
from app import login_manager
from app.auth.models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



