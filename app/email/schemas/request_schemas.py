from app.common.custom_classes import BaseModelDocumentable


class ResendRequest(BaseModelDocumentable):
    email: str
