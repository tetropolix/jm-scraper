from typing import List, Optional
import werkzeug
from app.extensions import db
from app.products.models import (
    Brand,
    ProductData,
    Eshop,
    Gender,
    Product,
    ShoeSizeCm,
    ShoeSizeEu,
    ShoeSizeUk,
    ShoeSizeUs,
)
from scraping.schemas import FilterOptions
from operator import attrgetter
from sqlalchemy import func


def createProductFilterConditions(filterOptions: Optional[FilterOptions]) -> List:
    conditions = []
    if filterOptions == None:
        return conditions
    (brandName, name, gender,) = attrgetter(
        "brandName", "name", "gender"
    )(filterOptions)
    if name != None:
        conditions.append(Product.name.ilike("%" + filterOptions.name + "%"))
    if brandName != None and brandName != []:
        conditions.append(
            Product.brand.has(Brand.name.ilike(brandName))
            if isinstance(brandName, str)
            else Product.brand.has(
                func.lower(Brand.name).in_(map(str.lower, brandName))
            )
        )
    if gender != None and gender != []:  # Note - not sure if working properly!
        conditions.append(
            Product.genders.has(Gender.gender.ilike(gender))
            if isinstance(gender, str)
            else Product.genders.any(
                func.lower(Gender.gender).in_(map(str.lower, gender))
            )
        )
    return conditions


def createProductDataFilterConditions(filterOptions: Optional[FilterOptions]) -> List:
    conditions = []
    if filterOptions == None:
        return conditions
    (minPrice, maxPrice, percentOff, outOfStock, shoeSize, domain) = attrgetter(
        "minPrice",
        "maxPrice",
        "percentOff",
        "outOfStock",
        "shoeSize",
        "domain",
    )(filterOptions)
    if minPrice != None and maxPrice != None:
        conditions.append(ProductData.original_price.between(minPrice, maxPrice))
    elif minPrice != None:
        conditions.append(ProductData.original_price >= minPrice)
    elif maxPrice != None:
        conditions.append(ProductData.original_price <= maxPrice)
    if percentOff != None:
        conditions.append(ProductData.percent_off >= percentOff)
    if outOfStock != None:
        conditions.append(ProductData.out_of_stock == outOfStock)
    if domain != None and domain != []:
        conditions.append(
            ProductData.eshop.has(Eshop.domain.ilike(domain))
            if isinstance(domain, str)
            else ProductData.eshop.has(
                func.lower(Eshop.domain).in_(map(str.lower, domain))
            )
        )
    if len(shoeSize.us) > 0:  # Note - not sure if working properly!
        conditions.append(
            ProductData.shoe_sizes_us.any(
                func.lower(ShoeSizeUs.value).in_(map(str.lower, shoeSize.us))
            )
        )
    if len(shoeSize.uk) > 0:  # Note - not sure if working properly!
        conditions.append(
            ProductData.shoe_sizes_uk.any(
                func.lower(ShoeSizeUk.value).in_(map(str.lower, shoeSize.uk))
            )
        )
    if len(shoeSize.eu) > 0:  # Note - not sure if working properly!
        conditions.append(
            ProductData.shoe_sizes_eu.any(
                func.lower(ShoeSizeEu.value).in_(map(str.lower, shoeSize.eu))
            )
        )
    if len(shoeSize.cm) > 0:  # Note - not sure if working properly!
        conditions.append(
            ProductData.shoe_sizes_cm.any(
                func.lower(ShoeSizeCm.value).in_(map(str.lower, shoeSize.cm))
            )
        )
    return conditions


def queryProductMinPrice(productId: int) -> Optional[float]:
    if productId == None or type(productId) != int:
        return None
    productData = (
        ProductData.query.order_by(
            ProductData.scraped_at.desc(), ProductData.final_price.asc()
        )
        .filter(ProductData.product_id == productId)
        .first()
    )
    return productData.final_price if productData != None else None


def queryLatestProductDataForProduct(product: Product, conditions=[]):
    if product == None:
        return None
    return (
        product.product_data.order_by(ProductData.scraped_at.desc())
        .filter(*conditions)
        .first()
    )


def queryProductById(id: int):
    try:
        id = int(id)
        return Product.query.get(id)
    except ValueError as e:
        print(e)
        return None


def paginateProductsWithProductData(
    page: int = 1, productsPerPage: int = 20, filterOptions: FilterOptions = None
) -> Optional[dict]:
    if productsPerPage < 1 or productsPerPage > 32:
        None
    output = {"products": {}}
    productConditions = createProductFilterConditions(filterOptions)
    productDataConditions = createProductDataFilterConditions(filterOptions)
    latestProductDataForProducts = (
        db.session.query(func.max(ProductData.scraped_at), ProductData.product_id)
        .group_by(ProductData.product_id)
        .all()
    )
    productsQuery = (
        Product.query.distinct()
        .filter(*productConditions)
        .join(Product.product_data)
        .filter(
            *productDataConditions,
        )
    ).filter(
        Product.id.in_(
            map(
                lambda productData: productData.product_id,
                latestProductDataForProducts,
            )
        )
    )
    try:
        products = productsQuery.paginate(page=page, per_page=productsPerPage)
    except werkzeug.exceptions.HTTPException:
        return None
    for product in products.items:
        productData = queryLatestProductDataForProduct(
            product, conditions=productDataConditions
        )
        if productData != None:
            output["products"][product] = productData
    output["current_page"] = products.page
    output["total_pages"] = products.pages
    output["total_items"] = products.total
    return output


def get_latest_product_data() -> List[ProductData]:
    return ProductData.query.order_by(ProductData.scraped_at.desc()).all()


def query_filter_options() -> dict:
    res = {}
    latest_product_data = get_latest_product_data()
    res["brandName"] = [brand.name for brand in Brand.query.all()]
    res["maxPrice"] = max((pd.final_price for pd in latest_product_data), default=0)
    res["minPrice"] = min((pd.final_price for pd in latest_product_data), default=0)
    res["maxPercentOff"] = max(
        (pd.percent_off for pd in latest_product_data), default=0
    )
    res["isSomethingOutOfStock"] = next(
        (True for pd in latest_product_data if pd.out_of_stock), False
    )
    res["isSomethingInStock"] = next(
        (True for pd in latest_product_data if not pd.out_of_stock), False
    )
    res["shoeSizes"] = {
        "us": [size.value for size in ShoeSizeUs.query.all()],
        "uk": [size.value for size in ShoeSizeUk.query.all()],
        "eu": [size.value for size in ShoeSizeEu.query.all()],
        "cm": [size.value for size in ShoeSizeCm.query.all()],
    }
    res["genders"] = [g.gender for g in Gender.query.all()]
    res["domains"] = [eshop.domain for eshop in Eshop.query.all()]
    return res
