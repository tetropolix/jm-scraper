from datetime import date, datetime
from typing import List, Set, Optional, Literal, Union
from pydantic import BaseModel, validator, root_validator

# REQUESTS
class ProductsRequest(BaseModel):
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


#####################

# UTILS


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


######################


# RESPONSE
class ErrorResponse(BaseModel):
    error: bool = False
    errorMessage: Optional[str]


class ProductsResponse(ErrorResponse):
    products: List[Product] = []
    current_page: int = 0
    total_pages: int = 0
    total_items: int = 0


class ProductResponse(ErrorResponse):
    product: Optional[Product]


#######################
