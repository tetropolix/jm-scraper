from app.products.models import Product
from app.profile.schemas import ProductRequest
from app.auth.models import User
from app.extensions import db
from typing import List


def verify_max_products_per_profile(request: ProductRequest, user: User) -> bool:
    user_profile = user.profile
    return len(request.product_ids) + len(user_profile.products) <= 20


def add_products_for_profile(request: ProductRequest, user: User) -> List[int]:
    product_ids = (
        request.product_ids
        if isinstance(request.product_ids, list)
        else [request.product_ids]
    )
    products = Product.query.filter(Product.id.in_(product_ids)).all()
    user_profile = user.profile
    user_profile_product_ids_before_insert = [
        product.id for product in user_profile.products
    ]
    user_profile.products.extend(products)
    db.session.add(user_profile)
    db.session.commit()
    return list(
        set([product.id for product in user_profile.products])
        - set(user_profile_product_ids_before_insert)
    )


def remove_products_from_profile(request: ProductRequest, user: User):
    product_ids = (
        request.product_ids
        if isinstance(request.product_ids, list)
        else [request.product_ids]
    )
    user_profile = user.profile
    user_profile_product_ids_before_remove = [
        product.id for product in user_profile.products
    ]
    user_profile.products = [
        prod for prod in user_profile.products if prod.id not in product_ids
    ]
    db.session.add(user_profile)
    db.session.commit()
    return list(
        set(user_profile_product_ids_before_remove)
        - set([product.id for product in user_profile.products])
    )
