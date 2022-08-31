from app.common.custom_classes import BaseModelDocumentable


class ConfirmationResponse(BaseModelDocumentable):
    already_confirmed: bool = False
    confirmed: bool = False
    invalid_token: bool = False  # token was tampered or already expired
    
