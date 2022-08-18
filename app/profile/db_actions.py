import validators

from ..common.schemas import ProductWithoutProductData

from .schemas.response_schemas import UserProfileProductsResponse

from ..common.exceptions import NotValidUrlPathError
from .models import PredefinedProfileFilters, Profile
from .schemas.common import PredefinedProfileFilters as PredefinedProfileFiltersSchema
from app.profile.schemas.request_schemas import (
    UserProfileProductsRequest,
    UserProfileRequest,
)
from app.products.models import (
    Brand,
    Eshop,
    Gender,
    Product,
    ShoeSizeCm,
    ShoeSizeEu,
    ShoeSizeUk,
    ShoeSizeUs,
)
from app.auth.models import User
from app.extensions import db
from typing import List, Literal, Tuple, Union


def verify_max_products_per_profile(
    request: UserProfileProductsRequest, user: User
) -> bool:
    user_profile: Profile = user.profile
    profile_products_max = user_profile.max_products
    return (
        len(request.product_ids_list) + len(user_profile.products)
        <= profile_products_max
    )


def query_list_of_shoe_sizes_for_profile(
    sizes: List[str], metric: Literal["us", "eu", "cm", "uk"]
) -> List[Union[ShoeSizeUs, ShoeSizeEu, ShoeSizeUk, ShoeSizeCm]]:
    if metric == "us":
        ShoeSizeModel = ShoeSizeUs
    elif metric == "uk":
        ShoeSizeModel = ShoeSizeUk
    elif metric == "eu":
        ShoeSizeModel = ShoeSizeEu
    elif metric == "cm":
        ShoeSizeModel = ShoeSizeCm
    else:
        raise ValueError(
            "Unrecognized metric, available values are ['us','eu','cm','uk']"
        )
    return ShoeSizeModel.query.filter(ShoeSizeModel.value.in_(sizes)).all()


def update_products_for_profile(
    req: UserProfileProductsRequest, user: User
) -> Tuple[List[ProductWithoutProductData], int, int]:
    user_profile: Profile = user.profile
    max_products = user_profile.max_products
    product_ids = req.product_ids_list
    number_of_products_before_update = len(user_profile.products)
    if req.remove:
        user_profile.products = [
            prod for prod in user_profile.products if prod.id not in product_ids
        ]
    elif req.add:
        products = Product.query.filter(Product.id.in_(product_ids)).all()
        user_profile.products.extend(products)
    db.session.commit()
    number_of_products_after_update = len(user_profile.products)
    num_of_affected_products = (
        number_of_products_after_update - number_of_products_before_update
        if req.add
        else number_of_products_before_update - number_of_products_after_update,
    )
    return (user_profile.products, num_of_affected_products, max_products)


def update_user_profile_personal_info(
    request: UserProfileRequest, user: User
) -> Profile:
    user_profile: Profile = user.profile
    if request.avatarUri:
        if not validators.url(request.avatarUri):
            raise NotValidUrlPathError("Invalid path for avatar URI")
        user_profile.avatar_uri = request.avatarUri
    if request.gender:
        user_profile.gender = request.gender
    if request.birthDate:
        user_profile.birth_date = request.birthDate
    if request.sendNotifications:
        user_profile.send_notifications = request.sendNotifications
    db.session.commit()
    return user_profile


def update_user_profile_predefined_filters(
    request: UserProfileRequest, user: User
) -> Profile:
    user_profile: Profile = user.profile
    ppf: PredefinedProfileFilters = user_profile.predefined_profile_filters
    req_ppf: PredefinedProfileFiltersSchema = request.predefinedProfileFilters
    if req_ppf.maxPrice:
        ppf.max_price = req_ppf.maxPrice
    if req_ppf.minPrice:
        ppf.min_price = req_ppf.minPrice
    if req_ppf.maxPercentOff:
        ppf.percent_off = req_ppf.maxPercentOff
    if req_ppf.outOfStock:
        ppf.out_of_stock = req_ppf.outOfStock
    if req_ppf.shoeSizesUs:
        ppf.shoe_size_us = query_list_of_shoe_sizes_for_profile(
            req_ppf.shoeSizesUs, "us"
        )
    if req_ppf.shoeSizesUk:
        ppf.shoe_size_uk = query_list_of_shoe_sizes_for_profile(
            req_ppf.shoeSizesUk, "uk"
        )
    if req_ppf.shoeSizesEu:
        ppf.shoe_size_eu = query_list_of_shoe_sizes_for_profile(
            req_ppf.shoeSizesEu, "eu"
        )
    if req_ppf.shoeSizesCm:
        ppf.shoe_size_cm = query_list_of_shoe_sizes_for_profile(
            req_ppf.shoeSizesCm, "cm"
        )
    if req_ppf.brands:
        ppf.brands = Brand.query.filter(Brand.name.in_(req_ppf.brands)).all()
    if req_ppf.genders:
        ppf.genders = Gender.query.filter(Gender.gender.in_(req_ppf.genders)).all()
    if req_ppf.domains:
        ppf.eshops = Eshop.query.filter(Eshop.domain.in_(req_ppf.domains)).all()
    db.session.commit()
    return user_profile
