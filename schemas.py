from typing import Optional
from pydantic import BaseModel, ValidationError


class ShoeProduct(BaseModel):
    brandName: str
    name: str
    sku: Optional[str]
    smallImageUrl: str
    url: str
    finalPrice: int
    originalPrice: Optional[int]
    percentOff: Optional[int]
    outOfStock: Optional[bool] = False
    domain: str


def createShoeProduct(dictWithValues: dict) -> Optional[ShoeProduct]:
    try:
        return ShoeProduct(**dictWithValues)
    except ValidationError as e:
        print(e.json())
        return None
