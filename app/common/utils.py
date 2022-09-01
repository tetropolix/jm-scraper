from pydantic import ValidationError
from app.common.custom_responses import StatusCodeResponse
from .schemas import ProductWithoutProductData
from ..products.models import Product
from flask import Request, abort
from typing import TypeVar

T = TypeVar("T")


def create_product_without_product_data(
    product: Product, create_dict=False
) -> ProductWithoutProductData:
    product_dict = {
        "name": product.name,
        "brand": product.brand.name,
        "productImageUrl": product.product_image_url,
        "id": product.id,
    }

    if create_dict:
        return product_dict
    else:
        return ProductWithoutProductData(**product_dict)


def get_request_obj(request: Request, schema_class: T) -> T:
    """Returns request object with specified schema type or aborts with status code 400"""
    args = request.get_json()
    try:
        return schema_class(**args)
    except ValidationError:
        abort(400)
