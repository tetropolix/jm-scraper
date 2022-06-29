from typing import List, Optional, Literal, Union
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
    eshopID: str
    shoeSize: List[float]
    gender: List[Literal["Man", "Woman", "Kids","Unknown","Men & Women"]]

def createShoeProduct(dictWithValues: dict) -> Optional[ShoeProduct]:
    try:
        return ShoeProduct(**dictWithValues)
    except ValidationError as e:
        print(e.json())
        return None


class FilterOptions(BaseModel):
    brandName: Optional[Union[str, List[str]]]
    name: Optional[str]
    finalPrice: Optional[int]
    percentOff: Optional[int]
    outOfStock: Optional[bool]
    shoeSize: Optional[Union[float, List[float]]]
    gender: Optional[Literal["Man", "Woman", "Kids"]]

    def __init__(self, **kwargs):
        wrongArguments = list(set(kwargs.keys()) - set(self.getOptions()))
        if len(wrongArguments) != 0:
            raise TypeError(
                "__init__() got an unexpected keyword arguments: " + str(wrongArguments)
            )
        super().__init__(**kwargs)

    @staticmethod
    def getOptions() -> List[str]:
        return [
            "brandName",
            "name",
            "finalPrice",
            "percentOff",
            "outOfStock",
            "shoeSize",
            "gender",
        ]


def createFilterOptions(dictWithValues: dict) -> Optional[FilterOptions]:
    try:
        return FilterOptions(**dictWithValues)
    except ValidationError as e:
        print(e.json())
        return None
    except TypeError as e:
        print(str(e))
        return None
