from typing import List, Set, Optional, Literal, Union
from pydantic import validator

from app.common.custom_classes import BaseModelDocumentable
from .common import ProductsSort


class ProductsRequest(BaseModelDocumentable):
    page: Optional[int]
    productsPerPage: Optional[int]
    brandName: Optional[Union[str, List[str]]]
    name: Optional[str]
    minPrice: Optional[float]
    maxPrice: Optional[float]
    percentOff: Optional[float]
    outOfStock: Optional[bool]
    size_us: Optional[Set[str]]
    size_uk: Optional[Set[str]]
    size_eu: Optional[Set[str]]
    size_cm: Optional[Set[str]]
    gender: Optional[
        Union[
            Literal["Man", "Woman", "Kids", "Unknown"],
            List[Literal["Man", "Woman", "Kids", "Unknown"]],
        ]
    ]
    domain: Optional[Union[str, List[str]]]
    productsSort: Optional[ProductsSort]

    @validator("page")
    def valid_page_number(cls, v):
        if v < 1:
            raise ValueError("Page must be positive integer")
        return v

    @validator("productsPerPage")
    def valid_productsPerPage_number(cls, v):
        if v < 1:
            raise ValueError("productsPerPage must be positive integer")
        return v

    @validator("minPrice")
    def valid_minPrice_number(cls, v):
        if v < 0:
            raise ValueError("minPrice must be positive")
        return v

    @validator("maxPrice")
    def valid_maxPrice_number(cls, v):
        if v < 0:
            raise ValueError("maxPrice must be positive")
        return v
