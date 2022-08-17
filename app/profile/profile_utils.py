from app.auth.models import User
from app.common.utils import create_product_without_product_data
from app.profile.models import PredefinedProfileFilters, Profile
from app.profile.schemas.response_schemas import ProductResponse
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


def create_predefined_profile_filters_dict_from_profile(profile: Profile) -> dict:
    ppf: PredefinedProfileFilters = profile.predefined_profile_filters
    return {
        "minPrice": ppf.min_price,
        "maxPrice": ppf.max_price,
        "maxPercentOff": ppf.percent_off,
        "outOfStock": ppf.out_of_stock,
        "shoeSizesUs": [size.value for size in ppf.shoe_size_us],
        "shoeSizesUk": [size.value for size in ppf.shoe_size_uk],
        "shoeSizesEu": [size.value for size in ppf.shoe_size_eu],
        "shoeSizesCm": [size.value for size in ppf.shoe_size_cm],
        "genders": [gender.gender for gender in ppf.genders],
        "domains": [eshop.domain for eshop in ppf.eshops],
        "brands": [brand.name for brand in ppf.brands],
    }


def get_user_profile_dict(user: User) -> dict:
    user_profile: Profile = user.profile

    return {
        "birthDate": user_profile.birth_date,
        "avatarUri": user_profile.avatar_uri,
        "gender": user_profile.gender,
        "sendNotifications": user_profile.send_notifications,
        "products": [
            create_product_without_product_data(product, create_dict=True)
            for product in user_profile.products
        ],
        "predefinedProfileFilters": create_predefined_profile_filters_dict_from_profile(
            user_profile
        ),
    }
