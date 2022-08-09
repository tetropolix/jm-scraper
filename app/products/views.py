from flask import abort, request
from pydantic import ValidationError

from app.products.schemas import ProductResponse, ProductsRequest, ProductsResponse
from .db_actions import (
    paginateProductsWithProductData,
    queryLatestProductDataForProduct,
    queryProductById,
)
from .products_utils import (
    checkIfFilterShoudBeApplied,
    createErrorProductResponse,
    createErrorProductsResponse,
    createFilterOptionsFromArgs,
    createProduct,
    createProductResponse,
    createProductsResponse,
)
from app.products import products_bp


@products_bp.route("/products", methods=["POST"])
def products():
    # Check content type of request
    if request.content_type != "application/json":
        return (
            createErrorProductsResponse("Wrong content-type used"),
            400,
        )

    args = request.get_json()
    # try to create valid request format from given body
    try:
        args = ProductsRequest(**args)
    except ValidationError:
        return (
            createErrorProductsResponse("Wrong filter parameters"),
            400,
        )
    page = args.page or 1
    productsPerPage = args.productsPerPage or 20
    filterOptions = None
    # check for filter and create filter options if necessary
    applyFilter = checkIfFilterShoudBeApplied(args)
    if applyFilter:
        filterOptions = createFilterOptionsFromArgs(args)
    if applyFilter and filterOptions == None:
        return (
            createErrorProductsResponse("Cannot construct filter options!"),
            400,
        )
    # get paginated data
    result = paginateProductsWithProductData(
        page, productsPerPage, filterOptions=filterOptions
    )
    # error when accesing paginated data
    if result == None:
        return createErrorProductsResponse("Page not found!"), 404
    # creation of response from paginated data
    response = createProductsResponse(result)
    if response is None:
        return (
            createErrorProductsResponse("Server error occured while processing data"),
            500,
        )
    else:
        return response, 200


@products_bp.route("/product/<int:productId>", methods=["GET"])
def product(productId: int):
    product = queryProductById(productId)
    productData = queryLatestProductDataForProduct(product)
    # Product not found
    if product == None or productData == None:
        return createErrorProductResponse("Product was not found!"), 400
    # Try to create product response from acuiared data
    response = createProductResponse(product, productData)
    if response is None:
        return (
            createErrorProductsResponse(
                "Server error occured while searching for product"
            ),
            500,
        )
    else:
        return response, 200
