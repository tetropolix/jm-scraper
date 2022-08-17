from pydantic import ValidationError
from app.products.schemas import (
    ProductResponse,
    ProductsRequest,
    ProductsResponse,
)
from app.common.schemas import Product, ProductData
from scraping.schemas import (
    FilterOptions,
    createFilterOptions,
    createShoeSize,
)
from typing import Optional


def checkIfFilterShoudBeApplied(args: dict) -> bool:
    allowedFilterQueryParameters = [
        "brandName",
        "name",
        "minPrice",
        "maxPrice",
        "percentOff",
        "outOfStock",
        "gender",
        "domain",
        "size_us",
        "size_uk",
        "size_eu",
        "size_cm",
    ]
    for param in allowedFilterQueryParameters:
        if getattr(args, param, None) != None:
            return True
    return False


def createFilterOptionsFromArgs(args: ProductsRequest) -> Optional[FilterOptions]:
    shoeSize = createShoeSize(
        {
            "us": args.size_us if args.size_us else set(),
            "uk": args.size_uk if args.size_uk else set(),
            "eu": args.size_eu if args.size_eu else set(),
            "cm": args.size_cm if args.size_cm else set(),
        }
    )
    filterOptions = createFilterOptions(
        {
            "brandName": args.brandName,
            "name": args.name,
            "minPrice": args.minPrice,
            "maxPrice": args.maxPrice,
            "percentOff": args.percentOff,
            "outOfStock": args.outOfStock,
            "shoeSize": shoeSize,
            "gender": args.gender,
            "domain": args.domain,
        }
    )
    return filterOptions if all([shoeSize, filterOptions]) else None


def createProduct(product: dict, productData: dict) -> Optional[Product]:
    try:
        product = Product(
            **{
                "name": product.name,
                "brand": product.brand.name,
                "productImageUrl": product.product_image_url,
                "id": product.id,
                "productData": ProductData(
                    **{
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
                    }
                ),
            }
        )
        return product
    except ValidationError:
        return None


def createProductsResponse(result: dict, to_dict=True) -> Optional[ProductsResponse]:
    try:
        products = [
            createProduct(product, productData)
            for product, productData in result["products"].items()
        ]
        productsResponse = ProductsResponse(
            **{
                "products": products,
                "current_page": result["current_page"],
                "total_pages": result["total_pages"],
                "total_items": result["total_items"],
            }
        )
        return productsResponse.dict() if to_dict else productsResponse
    except ValidationError:
        return None


def createProductResponse(product: dict, productData: dict, to_dict=True):
    try:
        productResponse = ProductResponse(product=createProduct(product, productData))
        return productResponse.dict() if to_dict else productResponse
    except ValidationError:
        return None
