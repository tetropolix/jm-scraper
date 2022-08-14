from datetime import datetime
from typing import List, Literal, Optional

from app.common.custom_classes import BaseModelDocumentable


class ProductResponse(BaseModelDocumentable):
    added: bool = False
    removed: bool = False
    product_ids: Optional[List[int]] = None


class UserProfileResponse(BaseModelDocumentable):
    birth_date: Optional[datetime]
    avatar_uri: Optional[str]
    genders: List[Literal["Man", "Woman", "Kids", "Unknown"]]
    product_ids: List[int] = []
