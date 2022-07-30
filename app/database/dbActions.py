from datetime import datetime
from typing import Dict, List, Optional
from app import create_app, db
from app.database.models import (
    Brand,
    Eshop,
    Gender,
    Product,
    ProductData,
    ShoeSizeCm,
    ShoeSizeEu,
    ShoeSizeUk,
    ShoeSizeUs,
)
from scraping.schemas import (
    FilterOptions,
    ShoeProduct,
    ShoeSize,
    createShoeProduct,
    createShoeSize,
)
from math import ceil
from operator import attrgetter
from sqlalchemy import func


def createProductFilterConditions(filterOptions: FilterOptions) -> List:
    conditions = []
    (brandName, name, gender,) = attrgetter(
        "brandName", "name", "gender"
    )(filterOptions)
    if name != None:
        conditions.append(Product.name.ilike(filterOptions.name))
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


def createProductDataFilterConditions(filterOptions: FilterOptions) -> List:
    conditions = []
    (minPrice, maxPrice, percentOff, outOfStock, shoeSize, domain) = attrgetter(
        "minPrice",
        "maxPrice",
        "percentOff",
        "outOfStock",
        "shoeSize",
        "domain",
    )(filterOptions)
    if minPrice != None:
        conditions.append(ProductData.original_price >= minPrice)
    if maxPrice != None:
        conditions.append(ProductData.original_price <= maxPrice)
    if percentOff != None:
        conditions.append(ProductData.percent_off >= percentOff)
    if outOfStock != None:
        conditions.append(ProductData.out_of_stock == outOfStock)
    if domain != None and domain != []:
        conditions.append(
            ProductData.eshop.has(func.lower(Eshop.domain).in_(map(str.lower, domain)))
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


def insertBrand(brandName: str) -> int:
    brand = Brand.query.filter(Brand.name.ilike(brandName)).first()
    if brand == None:
        newBrand = Brand(name=brandName)
        db.session.add(newBrand)
        db.session.commit()
        return newBrand.id
    return brand.id


def queryGenders(genders: List[str]) -> List[Gender]:
    return Gender.query.filter(Gender.gender.in_(genders)).all()


def queryShoeSizesUs(sizes: List[float]) -> List[ShoeSizeUs]:
    return ShoeSizeUs.query.filter(ShoeSizeUs.value.in_(sizes)).all()


def queryShoeSizesUk(sizes: List[float]) -> List[ShoeSizeUk]:
    return ShoeSizeUk.query.filter(ShoeSizeUk.value.in_(sizes)).all()


def queryShoeSizesCm(sizes: List[float]) -> List[ShoeSizeCm]:
    return ShoeSizeCm.query.filter(ShoeSizeCm.value.in_(sizes)).all()


def queryShoeSizesEu(sizes: List[str]) -> List[ShoeSizeEu]:
    return ShoeSizeEu.query.filter(ShoeSizeEu.value.in_(sizes)).all()


def addShoeSizesForProductData(
    productSizes: ShoeSize, productData: ProductData
) -> ProductData:
    productSizes = productSizes.toDict()
    for sizeMetric in productSizes.keys():
        if sizeMetric == "us":
            productData.shoe_sizes_us.extend(queryShoeSizesUs(productSizes[sizeMetric]))
        elif sizeMetric == "uk":
            productData.shoe_sizes_uk.extend(queryShoeSizesUk(productSizes[sizeMetric]))
        elif sizeMetric == "cm":
            productData.shoe_sizes_cm.extend(queryShoeSizesCm(productSizes[sizeMetric]))
        elif sizeMetric == "eu":
            productData.shoe_sizes_eu.extend(queryShoeSizesEu(productSizes[sizeMetric]))
    return productData


def insertProduct(shoe: ShoeProduct) -> int:
    product = Product.query.filter_by(shoe_id=shoe.shoeId).first()
    if product == None:  # Product not in database
        brandId = insertBrand(shoe.brandName)
        newProduct = Product(
            name=shoe.name,
            brand_id=brandId,
            shoe_id=shoe.shoeId,
            product_image_url=shoe.smallImageUrl,
        )
        genders = queryGenders(shoe.gender)
        newProduct.genders.extend(genders)
        db.session.add(newProduct)
        db.session.commit()
        return newProduct.id
    return product.id


def insertProductData(
    productId: int, shoe: ShoeProduct, scrapedAt: datetime, eshops: dict
) -> Optional[int]:
    if not isinstance(productId, int):
        return None
    domain = shoe.domain
    eshopId = eshops.get(domain)
    if eshopId == None:
        return None
    productData = ProductData(
        scraped_at=scrapedAt,
        product_url=shoe.url,
        final_price=shoe.finalPrice,
        original_price=shoe.originalPrice,
        percent_off=shoe.percentOff,
        out_of_stock=shoe.outOfStock,
        product_id=productId,
        eshop_id=eshopId,
    )
    productData = addShoeSizesForProductData(shoe.shoeSize, productData)
    db.session.add(productData)
    db.session.commit()
    return productData.id


def queryEshops() -> List[Eshop]:
    return Eshop.query.all()


def getEshopsDict() -> dict:
    """
    returns dict in format {'domain':'eshop_id'}
    """
    eshops = queryEshops()
    return {eshop.domain: eshop.id for eshop in eshops}


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
    page: int, productsPerPage: int, filterOptions: FilterOptions = None
) -> Optional[Dict[Product, ProductData]]:
    count = Product.query.count()
    output = {}
    if page > ceil(count / productsPerPage):
        return None
    if filterOptions == None:
        products = Product.query.paginate(page=page, per_page=productsPerPage)
    else:
        productConditions = createProductFilterConditions(filterOptions)
        products = Product.query.filter(*productConditions).paginate(
            page=page, per_page=productsPerPage
        )
    for product in products.items:
        productDataConditions = createProductDataFilterConditions(filterOptions)
        productData = queryLatestProductDataForProduct(
            product, conditions=productDataConditions
        )
        if productData != None:
            print(productData.eshop.domain)
            output[product] = productData
    return output

#TESTING PURPOSES
if __name__ == "__main__":
    sz = createShoeSize(
        {
            "us": ["7", "10.5", "4.5", "7.5", "6.5", "6", "5"],
            "uk": [],
            "cm": [],
            "eu": ["38.5", "39", "38", "40", "36", "44", "36.5"],
        }
    )
    sp = createShoeProduct(
        {
            "brandName": "str",
            "name": "str",
            "shoeId": "ABC",
            "smallImageUrl": "str",
            "url": "str",
            "finalPrice": 15.9,
            "originalPrice": 15.2,
            "percentOff": 0.2,
            "domain": "https://www.footshop.sk",
            "eshopId": "str",
            "outOfStock": True,
            "shoeSize": sz,
            "gender": ["Man", "Woman"],
        }
    )
    app = create_app("development")
    with app.app_context():
        eshops = getEshopsDict()
        id = insertProduct(sp)
        productDataId = insertProductData(id, sp, datetime.now(), eshops)
        print(id, productDataId)
