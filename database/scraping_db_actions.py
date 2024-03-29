from datetime import datetime
from typing import List, Optional, Tuple
from app.extensions import db
from app.products.models import (
    Brand,
    Eshop,
    Gender,
    Product,
    ProductData,
    Scrape,
    ShoeSizeCm,
    ShoeSizeEu,
    ShoeSizeUk,
    ShoeSizeUs,
    shoe_size_cm_product_data,
    shoe_size_eu_product_data,
    shoe_size_uk_product_data,
    shoe_size_us_product_data,
)
from scraping.schemas import ShoeProduct, ShoeSize


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


def insertProduct(shoe: ShoeProduct) -> Tuple[int, bool]:
    """Inserts product into DB and returns tuple - (product_id,newly_inserted)"""
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
        return newProduct.id, True
    return product.id, False


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


def remove_products_with_product_data() -> Tuple[int, int]:
    """Returns tuple (products deleted,product data deleted)"""
    product_data_deleted = ProductData.query.delete()
    products_deleted = Product.query.delete()
    db.session.commit()
    return products_deleted, product_data_deleted


def insert_data_about_scrape(
    scraped_at: datetime,
    products_scraped: int,
    product_data_scraped: int,
    scrape_length_secs: int,
    products_count: int,
) -> Optional[int]:
    scrape = Scrape(
        scraped_at=scraped_at,
        products_scraped=products_scraped,
        product_data_scraped=product_data_scraped,
        scrape_length_secs=scrape_length_secs,
        products_count=products_count,
    )
    db.session.add(scrape)
    db.session.commit()
    return scrape.id


def get_products_count():
    return db.session.query(Product).count()
