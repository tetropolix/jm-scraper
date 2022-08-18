from sqlalchemy.orm import configure_mappers, relationship, backref
from app.extensions import db
from app.auth.models import User
from app.products.models import (
    Gender,
    Product,
    ShoeSizeCm,
    ShoeSizeEu,
    ShoeSizeUk,
    ShoeSizeUs,
)

predefined_profile_filters_shoe_size_us = db.Table(
    "predefined_profile_filters_shoe_size_us",
    db.Column("id", db.Integer, primary_key=True),
    db.Column(
        "predefined_profile_filters_id",
        db.Integer,
        db.ForeignKey("predefined_profile_filters.id"),
    ),
    db.Column("shoe_size_us_id", db.Integer, db.ForeignKey("shoe_sizes_us.id")),
)
predefined_profile_filters_shoe_size_uk = db.Table(
    "predefined_profile_filters_shoe_size_uk",
    db.Column("id", db.Integer, primary_key=True),
    db.Column(
        "predefined_profile_filters_id",
        db.Integer,
        db.ForeignKey("predefined_profile_filters.id"),
    ),
    db.Column("shoe_size_uk_id", db.Integer, db.ForeignKey("shoe_sizes_uk.id")),
)
predefined_profile_filters_shoe_size_cm = db.Table(
    "predefined_profile_filters_shoe_size_cm",
    db.Column("id", db.Integer, primary_key=True),
    db.Column(
        "predefined_profile_filters_id",
        db.Integer,
        db.ForeignKey("predefined_profile_filters.id"),
    ),
    db.Column("shoe_size_cm_id", db.Integer, db.ForeignKey("shoe_sizes_cm.id")),
)
predefined_profile_filters_shoe_size_eu = db.Table(
    "predefined_profile_filters_shoe_size_eu",
    db.Column("id", db.Integer, primary_key=True),
    db.Column(
        "predefined_profile_filters_id",
        db.Integer,
        db.ForeignKey("predefined_profile_filters.id"),
    ),
    db.Column("shoe_size_eu_id", db.Integer, db.ForeignKey("shoe_sizes_eu.id")),
)

predefined_profile_filters_brand = db.Table(
    "predefined_profile_filters_brand",
    db.Column("id", db.Integer, primary_key=True),
    db.Column(
        "predefined_profile_filters_id",
        db.Integer,
        db.ForeignKey("predefined_profile_filters.id"),
    ),
    db.Column("brand_id", db.Integer, db.ForeignKey("brands.id")),
)

predefined_profile_filters_gender = db.Table(
    "predefined_profile_filters_gender",
    db.Column("id", db.Integer, primary_key=True),
    db.Column(
        "predefined_profile_filters_id",
        db.Integer,
        db.ForeignKey("predefined_profile_filters.id"),
    ),
    db.Column("gender_id", db.Integer, db.ForeignKey("genders.id")),
)

predefined_profile_filters_eshop = db.Table(
    "predefined_profile_filters_eshop",
    db.Column("id", db.Integer, primary_key=True),
    db.Column(
        "predefined_profile_filters_id",
        db.Integer,
        db.ForeignKey("predefined_profile_filters.id"),
    ),
    db.Column("eshop_id", db.Integer, db.ForeignKey("eshops.id")),
)

profile_gender = db.Table(
    "profile_gender",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("profile_id", db.Integer, db.ForeignKey("profiles.id")),
    db.Column("gender_id", db.Integer, db.ForeignKey("genders.id")),
)

profile_product = db.Table(
    "profile_product",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("profile_id", db.Integer, db.ForeignKey("profiles.id")),
    db.Column("product_id", db.Integer, db.ForeignKey("products.id")),
)


class PredefinedProfileFilters(db.Model):
    __tablename__ = "predefined_profile_filters"
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("profiles.id"))
    max_price = db.Column(db.Numeric(6, 2), nullable=True)
    min_price = db.Column(db.Numeric(6, 2), nullable=True)
    percent_off = db.Column(db.Numeric(4, 2), nullable=True)
    out_of_stock = db.Column(db.Boolean, nullable=False, default=False)
    shoe_size_us = relationship(
        "ShoeSizeUs",
        secondary=predefined_profile_filters_shoe_size_us,
        lazy="subquery",
        backref="predefined_profile_filters",
    )
    shoe_size_uk = relationship(
        "ShoeSizeUk",
        secondary=predefined_profile_filters_shoe_size_uk,
        lazy="subquery",
        backref="predefined_profile_filters",
    )
    shoe_size_eu = relationship(
        "ShoeSizeEu",
        secondary=predefined_profile_filters_shoe_size_eu,
        lazy="subquery",
        backref="predefined_profile_filters",
    )
    shoe_size_cm = relationship(
        "ShoeSizeCm",
        secondary=predefined_profile_filters_shoe_size_cm,
        lazy="subquery",
        backref="predefined_profile_filters",
    )
    genders = relationship(
        "Gender",
        secondary=predefined_profile_filters_gender,
        lazy="subquery",
        backref="predefined_profile_filters",
    )
    eshops = relationship(
        "Eshop",
        secondary=predefined_profile_filters_eshop,
        lazy="subquery",
        backref="predefined_profile_filters",
    )
    brands = relationship(
        "Brand",
        secondary=predefined_profile_filters_brand,
        lazy="subquery",
        backref="predefined_profile_filters",
    )


class Profile(db.Model):
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True)
    max_products = db.Column(db.Integer, nullable=False, default=20)
    birth_date = db.Column(db.DateTime, nullable=True, default=None)
    avatar_uri = db.Column(db.String(256), nullable=True, default=None)
    gender_id = db.Column(
        db.Integer, db.ForeignKey("genders.id"), nullable=True, default=None
    )
    gender = relationship("Gender", backref="profile", uselist=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = relationship("User", backref=backref("profile", uselist=False))
    send_notifications = db.Column(db.Boolean, nullable=False, default=False)
    products = relationship(
        "Product", secondary=profile_product, lazy="subquery", backref="profiles"
    )
    predefined_profile_filters = relationship(
        "PredefinedProfileFilters", uselist=False, backref="profile"
    )

    @classmethod
    def query_by_id(cls, id: int):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def query_by_user_id(cls, user_id: int):
        return cls.query.filter_by(id=user_id).first()


configure_mappers()
