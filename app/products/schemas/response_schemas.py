from typing import List, Optional
from app.common.general_schemas import BaseModelDocumentable
from .common import Product


class ProductsResponse(BaseModelDocumentable):
    products: List[Product] = []
    current_page: int = 0
    total_pages: int = 0
    total_items: int = 0


class ProductResponse(BaseModelDocumentable):
    product: Optional[Product]
