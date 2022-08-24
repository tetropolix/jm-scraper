from typing import Literal, Optional
from app.auth.schemas.common import User
from app.common.custom_classes import BaseModelDocumentable
from pydantic import validator


class LoginLogoutResponse(BaseModelDocumentable):
    logged: bool = False
    next: Optional[str] = None
    user: Optional[User] = None


class RegisterResponse(BaseModelDocumentable):
    registered: bool = False
    errorOnRegister: Optional[
        Literal[
            "EMAIL_IN_USE",
            "INVALID_EMAIL",
            "SHORT_PASSWORD",
            "EMPTY_USERNAME",
            "PASSWORD_NO_MATCH",
        ]
    ]
    user: Optional[User] = None

    @validator("errorOnRegister")
    def is_registered_false_on_error_message(cls, v, values):
        if v is not None and values["registered"]:
            raise ValueError(
                "Error message cannot be set when registered is set to True"
            )
        return v


class CheckEmailResponse(BaseModelDocumentable):
    isUsed: bool


class UnauthorizedResponse(BaseModelDocumentable):
    next: str
    handled: bool = True
