from ctypes import Union
from typing import List, Literal, Optional
from app.common.custom_classes import BaseModelDocumentable
from app.common.schemas import Product, ShoeSizes


class ProductsResponse(BaseModelDocumentable):
    products: List[Product] = []
    current_page: int = 0
    total_pages: int = 0
    total_items: int = 0


class ProductResponse(BaseModelDocumentable):
    product: Optional[Product]


class FiltersResponse(BaseModelDocumentable):
    brandName: List[str] = []
    minPrice: float = 0
    maxPrice: float = 0
    maxPercentOff: float = 0
    isSomethingOutOfStock: bool = False
    isSomethingInStock: bool = False
    shoeSizes: ShoeSizes = ShoeSizes()
    genders: List[Literal["Man", "Woman", "Kids", "Unknown"]] = []
    domains: List[str] = []
