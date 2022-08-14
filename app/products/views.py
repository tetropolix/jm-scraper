from flask import request
from pydantic import ValidationError
from app.common.decorators import register_route
from .schemas.common import ShoeSizes

from app.products.schemas.request_schemas import ProductsRequest
from app.products.schemas.response_schemas import (
    FiltersResponse,
    ProductResponse,
    ProductsResponse,
)
from .db_actions import (
    paginateProductsWithProductData,
    query_filter_options,
    queryLatestProductDataForProduct,
    queryProductById,
)
from .products_utils import (
    checkIfFilterShoudBeApplied,
    createFilterOptionsFromArgs,
    createProductResponse,
    createProductsResponse,
)
from app.products import products_bp
from app.common.custom_responses import StatusCodeResponse

DEFAULT_PAGE = 1
DEFAULT_PRODUCTS_PER_PAGE = 20


@register_route(
    products_bp, "", ProductsRequest, ProductsResponse, methods=["POST"]
)
def products():
    """Returns products based on filter options provided (if any)"""
    # try to parse json in body of request
    args = request.get_json()
    # try to create valid request format from given body
    try:
        args = ProductsRequest(**args)
    except ValidationError:
        return StatusCodeResponse(400)
    page = args.page or DEFAULT_PAGE
    productsPerPage = args.productsPerPage or DEFAULT_PRODUCTS_PER_PAGE
    filterOptions = None
    # check for filter and create filter options if necessary
    applyFilter = checkIfFilterShoudBeApplied(args)
    if applyFilter:
        filterOptions = createFilterOptionsFromArgs(args)
    if applyFilter and filterOptions == None:
        return StatusCodeResponse(400)
    # get paginated data
    result = paginateProductsWithProductData(
        page, productsPerPage, filterOptions=filterOptions
    )
    # error when accesing paginated data
    if result == None:
        return StatusCodeResponse(404)
    # creation of response from paginated data
    response = createProductsResponse(result)
    if response is None:
        return StatusCodeResponse(500)
    else:
        return response, 200


@register_route(
    products_bp, "/<int:productId>", None, ProductResponse, methods=["GET"]
)
def product(productId: int):
    """Returns product by ID specified as part of URL"""
    product = queryProductById(productId)
    productData = queryLatestProductDataForProduct(product)
    # Product not found
    if product == None or productData == None:
        return StatusCodeResponse(400)
    # Try to create product response from acuiared data
    response = createProductResponse(product, productData)
    if response is None:
        return StatusCodeResponse(500)
    else:
        return response, 200


@register_route(
    products_bp, "/filters", None, FiltersResponse, methods=["GET"]
)
def filters():
    """Returns filter options which can be used for filtering specified range of products"""
    filter_options_dict = query_filter_options()
    try:
        return FiltersResponse(**filter_options_dict).dict()
    except ValidationError:
        return StatusCodeResponse(
            500, "INTERNAL SERVER ERROR - Unable to provide filter options"
        )
