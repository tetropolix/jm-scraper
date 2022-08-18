from pydantic import validator
from app.common.custom_classes import BaseModelDocumentable


class CheckEmailRequest(BaseModelDocumentable):
    email: str


class LoginRequest(BaseModelDocumentable):
    email: str
    password: str


class RegisterRequest(BaseModelDocumentable):
    email: str
    username: str
    password: str
    retryPassword: str
