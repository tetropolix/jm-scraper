from app.common.custom_classes import BaseModelDocumentable


class TokenRequest(BaseModelDocumentable):
    email: str


class ConfirmationRequest(BaseModelDocumentable):
    token: str


class PassResetRequest(BaseModelDocumentable):
    email: str
    new_password: str
    token: str
