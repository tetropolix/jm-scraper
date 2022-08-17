from .schemas import ProductWithoutProductData
from ..products.models import Product


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
