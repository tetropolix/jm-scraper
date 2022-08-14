from datetime import datetime
from typing import List, Union, Optional

from app.common.custom_classes import BaseModelDocumentable


class ProductRequest(BaseModelDocumentable):
    product_ids: Union[int, List[int]]


class UpdateUserProfileRequest(BaseModelDocumentable):
    birth_date: Optional[datetime]
    avatar_uri: Optional[str]
