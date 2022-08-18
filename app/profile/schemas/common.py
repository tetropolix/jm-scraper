from datetime import datetime
from typing import List, Literal, Optional

from app.common.custom_classes import BaseModelDocumentable
from ...common.schemas import ProductWithoutProductData


class PredefinedProfileFilters(BaseModelDocumentable):
    minPrice: float = None
    maxPrice: float = None
    maxPercentOff: float = None
    outOfStock: bool = None
    shoeSizesUs: List[str] = None
    shoeSizesUk: List[str] = None
    shoeSizesEu: List[str] = None
    shoeSizesCm: List[str] = None
    genders: List[Literal["Man", "Woman", "Kids", "Unknown"]] = None
    domains: List[str] = None
    brands: List[str] = None


class UserProfile(BaseModelDocumentable):
    maxProducts: int
    birthDate: Optional[datetime] = None
    avatarUri: Optional[str] = None
    gender: Optional[Literal["Man", "Woman", "Kids", "Unknown"]] = None
    sendNotifications: bool = False
    products: List[ProductWithoutProductData] = []
    predefinedProfileFilters: PredefinedProfileFilters
