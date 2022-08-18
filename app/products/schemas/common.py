from typing import Optional

from pydantic import root_validator
from app.common.custom_classes import BaseModelDocumentable


class ProductsSort(BaseModelDocumentable):
    priceAsc: bool = False
    priceDesc: bool = False
    percentOffAsc: bool = False
    percentOffDesc: bool = False

    @root_validator
    def only_asc_or_desc(cls, values):
        priceAsc = values["priceAsc"]
        priceDesc = values["priceDesc"]
        percentOffAsc = values["percentOffAsc"]
        percentOffDesc = values["percentOffDesc"]
        if (priceAsc and priceDesc) or (percentOffAsc and percentOffDesc):
            raise ValueError(
                "Invalid values for sorting options - one parameter can be sorted only asc or desc"
            )
        return values
