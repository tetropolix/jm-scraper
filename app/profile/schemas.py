from typing import List, Union, Optional

from app.common.general_schemas import BaseModelDocumentable


class ProductRequest(BaseModelDocumentable):
    product_ids: Union[int, List[int]]


class ProductResponse(BaseModelDocumentable):
    added: bool = False
    removed: bool = False
    product_ids: Optional[List[int]] = None
