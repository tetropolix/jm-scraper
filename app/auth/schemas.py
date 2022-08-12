from typing import Optional
from pydantic import BaseModel

from app.common.general_schemas import BaseModelDocumentable


class User(BaseModel):
    email: str
    username: str


class LoginLogoutResponse(BaseModelDocumentable):
    logged: bool = False
    error: Optional[str] = None
    next: Optional[str] = None
    user: Optional[User] = None


class RegisterResponse(BaseModelDocumentable):
    registered: bool = False
    error: Optional[str] = None
    user: Optional[User] = None
