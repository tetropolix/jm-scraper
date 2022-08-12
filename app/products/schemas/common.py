from datetime import datetime
from typing import List
from pydantic import BaseModel


class ProductData(BaseModel):
    scrapedAt: datetime
    finalPrice: float
    originalPrice: float
    percentOff: float
    outOfStock: bool
    sizes_us: List[str] = []
    sizes_uk: List[str] = []
    sizes_eu: List[str] = []
    sizes_cm: List[str] = []


class Product(BaseModel):
    name: str
    brand: str
    productImageUrl: str
    id: int
    productData: ProductData
