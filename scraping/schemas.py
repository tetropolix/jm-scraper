import json
from typing import List, Set, Optional, Literal, Union
from pydantic import BaseModel, ValidationError, root_validator


class ShoeSize(BaseModel):
    us: Set[str] = set()
    uk: Set[str] = set()
    cm: Set[str] = set()
    eu: Set[str] = set()

    def isAnySizeListPopulated(self) -> bool:
        return any([self.us, self.uk, self.cm, self.eu])

    def toDict(self, setToList=True):
        if setToList == True:
            return {k: list(v) for k, v in dict(self).items()}
        return dict(self)


def createShoeSize(dictWithValues: dict) -> Optional[ShoeSize]:
    try:
        return ShoeSize(**dictWithValues)
    except ValidationError as e:
        print(e.json())
        return None


class ShoeProduct(BaseModel):
    brandName: str
    name: str
    shoeId: str
    smallImageUrl: str
    url: str
    finalPrice: float
    originalPrice: Optional[float]
    percentOff: Optional[float]
    domain: str
    eshopId: str
    outOfStock: Optional[bool] = False
    shoeSize: ShoeSize
    gender: List[Literal["Man", "Woman", "Kids", "Unknown"]]

    def toDict(self):
        shoeProduct = self.copy()
        shoeSize = self.shoeSize.toDict()
        shoeProduct.shoeSize = shoeSize
        return dict(shoeProduct)

    @root_validator
    def checkStockAndSizes(cls, values):
        if not any([values["shoeSize"].isAnySizeListPopulated(), values["outOfStock"]]):
            raise ValueError(
                "If outOfStock is False at least one size list for product must be populated!"
            )
        else:
            return values


def createShoeProduct(dictWithValues: dict) -> Optional[ShoeProduct]:
    try:
        return ShoeProduct(**dictWithValues)
    except ValidationError as e:
        print(e.json())
        return None


class FilterOptions(BaseModel):
    brandName: Optional[Union[str, List[str]]]
    name: Optional[str]
    minPrice: Optional[float]
    maxPrice: Optional[float]
    percentOff: Optional[float]
    outOfStock: Optional[bool]
    shoeSize: Optional[ShoeSize]
    gender: Optional[
        Union[
            Literal["Man", "Woman", "Kids", "Unknown"],
            List[Literal["Man", "Woman", "Kids", "Unknown"]],
        ]
    ]
    domain: Optional[Union[str, List[str]]]


def createFilterOptions(dictWithValues: dict) -> Optional[FilterOptions]:
    try:
        return FilterOptions(**dictWithValues)
    except ValidationError as e:
        print(e.json())
        return None


if __name__ == "__main__":
    # testing purposes
    sz = createShoeSize({"eu": []})
    sp = createShoeProduct(
        {
            "brandName": "str",
            "name": "str",
            "sku": "Optional[str]",
            "smallImageUrl": "str",
            "url": "str",
            "finalPrice": 15.9,
            "originalPrice": 15.2,
            "percentOff": 0.2,
            "domain": "str",
            "eshopId": "str",
            "outOfStock": True,
            "shoeSize": sz,
            "gender": ["Man"],
        }
    )
    print(sp.toDict())
    with open("scrapedData" + ".json", "w") as file:
        file.write(json.dumps(sp.toDict()))
    print(sz)
