from datetime import datetime
from typing import List
from .custom_classes import BaseModelDocumentable


class ProductData(BaseModelDocumentable):
    scrapedAt: datetime
    finalPrice: float
    originalPrice: float
    percentOff: float
    outOfStock: bool
    sizes_us: List[str] = []
    sizes_uk: List[str] = []
    sizes_eu: List[str] = []
    sizes_cm: List[str] = []


class Product(BaseModelDocumentable):
    name: str
    brand: str
    productImageUrl: str
    id: int
    productData: ProductData


class ShoeSizes(BaseModelDocumentable):
    us: List[str] = list()
    uk: List[str] = list()
    cm: List[str] = list()
    eu: List[str] = list()


class ProductWithoutProductData(BaseModelDocumentable):
    name: str
    brand: str
    productImageUrl: str
    id: int
