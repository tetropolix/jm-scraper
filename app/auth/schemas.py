from typing import List, Set, Optional, Literal, Union
from pydantic import BaseModel, ValidationError, root_validator


class User(BaseModel):
    email: str
    username: str


class LoginLogoutResponse(BaseModel):
    logged: bool = False
    error: Optional[str] = None
    next: Optional[str] = None
    user: Optional[User] = None


class RegisterReponse(BaseModel):
    registered: bool = False
    error: Optional[str] = None
    user: Optional[User] = None
