from typing import Optional
from app import app
from flask import abort, render_template, request
from scraping.schemas import (
    FilterOptions,
    createFilterOptions,
    createShoeSize,
)
from app.database.dbActions import (
    paginateProductsWithProductData,
    queryLatestProductDataForProduct,
    queryProductById,
)
from pprint import pprint


def checkIfFilterShoudBeApplied(args: dict) -> bool:
    allowedFilterQueryParameters = [
        "brandName",
        "name",
        "minPrice",
        "maxPrice",
        "percentOff",
        "outOfStock",
        "shoeSize",
        "gender",
        "domain",
        "us_size",
        "uk_size",
        "eu_size",
        "cm_size",
    ]
    for param in allowedFilterQueryParameters:
        if args.get(param) != None:
            return True
    return False


def createFilterOptionsFromArgs(args) -> Optional[FilterOptions]:
    try:
        shoeSize = createShoeSize(
            {
                "us": args.getlist("size_us", type=str),
                "uk": args.getlist("size_uk", type=str),
                "eu": args.getlist("size_eu", type=str),
                "cm": args.getlist("size_cm", type=str),
            }
        )
        filterOptions = createFilterOptions(
            {
                "brandName": args.getlist("brandName", type=str) or None,
                "name": args.get("name", None, type=str),
                "minPrice": args.get("minPrice", None, type=float),
                "maxPrice": args.get("maxPrice", None, type=float),
                "percentOff": args.get("percentOff", None, type=float),
                "outOfStock": args.get(
                    "outOfStock",
                    None,
                    type=lambda val: val.lower() == "true"
                    if val.lower() in ["true", "false"]
                    else val,  # returning val as string proceeds to ValueError exception
                ),
                "shoeSize": shoeSize,
                "gender": [
                    gender.capitalize() for gender in args.getlist("gender", type=str)
                ]
                or None,
                "domain": args.getlist("domain", type=str) or None,
            }
        )
    except ValueError as e:
        return None
    return filterOptions if all([shoeSize, filterOptions]) else None


@app.route("/products", methods=["GET"])
def products():
    try:
        page = request.args.get("page", 1, type=int)
        productsPerPage = request.args.get("productsPerPage", 20, type=int)
        if productsPerPage < 1 or productsPerPage > 64:
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
                },
            }
            for product, productData in products.items()
        ]
    }


@app.route("/product/<int:productId>", methods=["GET"])
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
