from pydantic import BaseModel, validator
from app.general_schemas import ErrorResponse
from typing import List, Union, Optional


class ProductRequest(BaseModel):
    product_ids: Union[int, List[int]]


class ProductResponse(ErrorResponse):
    added: bool = False
    removed: bool = False
    product_ids: Optional[List[int]] = None
