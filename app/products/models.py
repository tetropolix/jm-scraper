from sqlalchemy.orm import relationship, configure_mappers
from app.extensions import db

shoe_size_eu_product_data = db.Table(
    "shoe_size_eu_product_data",
    db.Column("id", db.Integer, primary_key=True),
    db.Column(
        "shoe_size_id",
        db.Integer,
        db.ForeignKey("shoe_sizes_eu.id", ondelete="CASCADE"),
    ),
    db.Column(
        "product_data_id",
        db.Integer,
        db.ForeignKey("product_data.id", ondelete="CASCADE"),
    ),
)

shoe_size_us_product_data = db.Table(
    "shoe_size_us_product_data",
    db.Column("id", db.Integer, primary_key=True),
    db.Column(
        "shoe_size_id",
        db.Integer,
        db.ForeignKey("shoe_sizes_us.id", ondelete="CASCADE"),
    ),
    db.Column(
        "product_data_id",
        db.Integer,
        db.ForeignKey("product_data.id", ondelete="CASCADE"),
    ),
)

shoe_size_uk_product_data = db.Table(
    "shoe_size_uk_product_data",
    db.Column("id", db.Integer, primary_key=True),
    db.Column(
        "shoe_size_id",
        db.Integer,
        db.ForeignKey("shoe_sizes_uk.id", ondelete="CASCADE"),
    ),
    db.Column(
        "product_data_id",
        db.Integer,
        db.ForeignKey("product_data.id", ondelete="CASCADE"),
    ),
)

shoe_size_cm_product_data = db.Table(
    "shoe_size_cm_product_data",
    db.Column("id", db.Integer, primary_key=True),
    db.Column(
        "shoe_size_id",
        db.Integer,
        db.ForeignKey("shoe_sizes_cm.id", ondelete="CASCADE"),
    ),
    db.Column(
        "product_data_id",
        db.Integer,
        db.ForeignKey("product_data.id", ondelete="CASCADE"),
    ),
)

product_gender = db.Table(
    "product_gender",
    db.Column("id", db.Integer, primary_key=True),
    db.Column(
        "product_id", db.Integer, db.ForeignKey("products.id", ondelete="CASCADE")
    ),
    db.Column("gender_id", db.Integer, db.ForeignKey("genders.id", ondelete="CASCADE")),
)


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey("brands.id"), nullable=False)
    shoe_id = db.Column(db.String(32), nullable=False, unique=True)
    product_image_url = db.Column(db.String(512), nullable=False)
    product_data = relationship("ProductData", backref="product", lazy="dynamic")
    genders = relationship(
        "Gender", secondary=product_gender, lazy="subquery", backref="products"
    )

    def __repr__(self):
        return "<Product with id (%d) (%s) with brand reference to (%d) >" % (
            self.id,
            self.name,
            self.brand_id,
        )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Brand(db.Model):
    __tablename__ = "brands"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True, nullable=False)
    products = relationship("Product", backref="brand", lazy=True)

    def __repr__(self):
        return "<Brand (%s)>" % self.name


class ProductData(db.Model):
    __tablename__ = "product_data"
    id = db.Column(db.Integer, primary_key=True)
    scraped_at = db.Column(db.DateTime, nullable=False)
    product_url = db.Column(db.String(512), nullable=False)
    final_price = db.Column(db.Numeric(6, 2), nullable=False)
    original_price = db.Column(db.Numeric(6, 2), nullable=True)
    percent_off = db.Column(db.Numeric(4, 2), nullable=True)
    out_of_stock = db.Column(db.Boolean, nullable=False)
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    eshop_id = db.Column(db.Integer, db.ForeignKey("eshops.id"), nullable=False)
    shoe_sizes_eu = relationship(
        "ShoeSizeEu",
        secondary=shoe_size_eu_product_data,
        lazy="subquery",
        backref="product_data",
    )
    shoe_sizes_us = relationship(
        "ShoeSizeUs",
        secondary=shoe_size_us_product_data,
        lazy="subquery",
        backref="product_data",
    )
    shoe_sizes_uk = relationship(
        "ShoeSizeUk",
        secondary=shoe_size_uk_product_data,
        lazy="subquery",
        backref="product_data",
    )
    shoe_sizes_cm = relationship(
        "ShoeSizeCm",
        secondary=shoe_size_cm_product_data,
        lazy="subquery",
        backref="product_data",
    )

    def __repr__(self):
        scrapedAt = self.scraped_at.strftime("%B %d %H:%M:%S, %Y")
        return "<ProductData with reference on %d product scraped at %s>" % (
            self.product_id,
            scrapedAt,
        )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Eshop(db.Model):
    __tablename__ = "eshops"
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(128), nullable=False, unique=True)
    eshop_logo_url = db.Column(db.String(512), nullable=False)
    product_data = relationship("ProductData", backref="eshop", lazy=True)

    def __repr__(self):
        return "<Eshop %s>" % self.domain


class ShoeSizeEu(db.Model):
    __tablename__ = "shoe_sizes_eu"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(16), nullable=False, unique=True)

    def __repr__(self):
        return "<Shoe size eu %s" % (self.value)


class ShoeSizeUs(db.Model):
    __tablename__ = "shoe_sizes_us"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(16), nullable=False, unique=True)

    def __repr__(self):
        return "<Shoe size us %s" % (self.value)


class ShoeSizeUk(db.Model):
    __tablename__ = "shoe_sizes_uk"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(16), nullable=False, unique=True)

    def __repr__(self):
        return "<Shoe size uk %s" % (self.value)


class ShoeSizeCm(db.Model):
    __tablename__ = "shoe_sizes_cm"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(16), nullable=False, unique=True)

    def __repr__(self):
        return "<Shoe size cm %s" % (self.value)


class Gender(db.Model):
    __tablename__ = "genders"
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(64), nullable=False, unique=True)

    def __repr__(self):
        return "<Gender %s>" % self.gender


class Scrape(db.Model):
    __tablename__ = "scrapes"
    id = db.Column(db.Integer, primary_key=True)
    scraped_at = db.Column(db.DateTime, nullable=False)
    products_scraped = db.Column(db.Integer, nullable=False)
    product_data_scraped = db.Column(db.Integer, nullable=False)
    scrape_length_secs = db.Column(db.Numeric(8, 2), nullable=False)
    products_count = db.Column(db.Integer, nullable=False)


configure_mappers()
