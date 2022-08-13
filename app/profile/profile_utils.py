from .schemas import ProductResponse
from typing import Optional, Union, List
from pydantic import ValidationError


def createProductResponse(
    product_ids: Union[int, List[int]],
    added: bool = False,
    removed: bool = False,
    to_dict: bool = True,
) -> Optional[ProductResponse]:
    try:
        response = ProductResponse(
            added=added, removed=removed, product_ids=product_ids
        )
        return response.dict() if to_dict else response
    except ValidationError:
        return None
