from flask import abort, request
from .db_actions import (
    paginateProductsWithProductData,
    queryLatestProductDataForProduct,
    queryProductById,
)
from .products_utils import (
    checkIfFilterShoudBeApplied,
    createFilterOptionsFromArgs,
)
from app.products import products_bp


@products_bp.route("/products", methods=["GET"])
def products():
    try:
        page = request.args.get("page", 1, type=int)
        productsPerPage = request.args.get("productsPerPage", 20, type=int)
        if productsPerPage < 1 or productsPerPage > 32:
            raise ValueError("Invalid value for for query parameter")
    except ValueError as e:
        abort(404, "Unable to process query parameters!")
    args = request.args
    filterOptions = None
    applyFilter = checkIfFilterShoudBeApplied(args.to_dict(flat=False))
    if applyFilter:
        filterOptions = createFilterOptionsFromArgs(args)
    if applyFilter and filterOptions == None:
        abort(404, "Cannot construct filter options!")
    products = paginateProductsWithProductData(
        page, productsPerPage, filterOptions=filterOptions
    )
    if products == None:
        abort(404, "Page not found!")
    return {
        "products": [
            {
                "name": product.name,
                "brand": product.brand.name,
                "productImageUrl": product.product_image_url,
                "id": product.id,
                "productData": {
                    "scrapedAt": productData.scraped_at,
                    "finalPrice": productData.final_price,
                    "originalPrice": productData.original_price,
                    "percentOff": productData.percent_off,
                    "outOfStock": productData.out_of_stock,
                    "sizes_us": [
                        us_size.value for us_size in productData.shoe_sizes_us
                    ],
                    "sizes_uk": [
                        uk_size.value for uk_size in productData.shoe_sizes_uk
                    ],
                    "sizes_eu": [
                        eu_size.value for eu_size in productData.shoe_sizes_eu
                    ],
                    "sizes_cm": [
                        cm_size.value for cm_size in productData.shoe_sizes_cm
                    ],
                },
            }
            for product, productData in products.items()
        ]
    }


@products_bp.route("/product/<int:productId>", methods=["GET"])
def product(productId: int):
    product = queryProductById(productId)
    productData = queryLatestProductDataForProduct(product)
    if product == None or productData == None:
        return {
            "error": True,
            "errorMessage": "Product was not found!",
            "product": None,
        }
    return {
        "error": False,
        "errorMessage": "",
        "product": {
            "name": product.name,
            "brand": product.brand.name,
            "productImageUrl": product.product_image_url,
            "id": product.id,
            "productData": {
                "scrapedAt": productData.scraped_at,
                "finalPrice": productData.final_price,
                "originalPrice": productData.original_price,
                "percentOff": productData.percent_off,
                "outOfStock": productData.out_of_stock,
                "sizes_us": [us_size.value for us_size in productData.shoe_sizes_us],
                "sizes_uk": [uk_size.value for uk_size in productData.shoe_sizes_uk],
                "sizes_eu": [eu_size.value for eu_size in productData.shoe_sizes_eu],
                "sizes_cm": [cm_size.value for cm_size in productData.shoe_sizes_cm],
            },
        },
    }
