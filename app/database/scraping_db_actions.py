from datetime import datetime
from typing import List, Optional
from app import db, create_app
from app.products.models import (
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
from scraping.schemas import ShoeProduct, ShoeSize, createShoeProduct, createShoeSize


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


# TESTING PURPOSES
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
    app = create_app("developmentLocal")
    with app.app_context():
        eshops = getEshopsDict()
        id = insertProduct(sp)
        productDataId = insertProductData(id, sp, datetime.now(), eshops)
        print(id, productDataId)
