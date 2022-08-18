from typing import List, Optional

from app.common.custom_classes import BaseModelDocumentable
from app.common.schemas import ProductWithoutProductData
from .common import UserProfile


class UserProfileProductsResponse(BaseModelDocumentable):
    maxProductsForProfile: int
    numberOfAffectedProducts: int
    products: List[ProductWithoutProductData] = []


class UserProfileResponse(BaseModelDocumentable):
    profile: UserProfile
