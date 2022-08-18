from datetime import datetime
from typing import List, Literal, Union, Optional

from pydantic import root_validator

from app.common.custom_classes import BaseModelDocumentable
from app.profile.schemas.common import PredefinedProfileFilters


class UserProfileProductsRequest(BaseModelDocumentable):
    product_ids: Union[int, List[int]]
    add: bool = False
    remove: bool = False

    @root_validator()
    def add_or_remove(cls, values):
        add = values["add"]
        remove = values["remove"]
        if add and remove or (not add and not remove):
            raise ValueError(
                "Invalid values for add and remove - both parameters cannot be same"
            )
        return values

    @property
    def product_ids_list(self):
        return (
            [self.product_ids]
            if isinstance(self.product_ids, int)
            else self.product_ids
        )


class UserProfileRequest(BaseModelDocumentable):
    birthDate: Optional[datetime] = None
    avatarUri: Optional[str] = None
    gender: Optional[Literal["Man", "Woman", "Kids", "Unknown"]] = None
    sendNotifications: Optional[bool] = None
    product_ids: Optional[List[int]] = None
    predefinedProfileFilters: Optional[PredefinedProfileFilters] = None

    def should_update_personal_info(self) -> bool:
        return bool(
            self.birthDate is not None
            or self.avatarUri is not None
            or self.gender is not None
            or self.sendNotifications is not None
        )

    def should_update_products(self) -> bool:
        return self.product_ids is not None

    def should_update_filters(self) -> bool:
        return self.predefinedProfileFilters is not None

    def number_of_sections_to_update(self) -> int:
        should_update_personal_info = self.should_update_personal_info()
        should_update_products = self.should_update_products()
        should_update_filters = self.should_update_filters()
        return [
            should_update_filters,
            should_update_personal_info,
            should_update_products,
        ].count(True)
