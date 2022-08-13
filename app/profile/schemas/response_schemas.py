from typing import List, Optional

from app.common.custom_classes import BaseModelDocumentable


class ProductResponse(BaseModelDocumentable):
    added: bool = False
    removed: bool = False
    product_ids: Optional[List[int]] = None
