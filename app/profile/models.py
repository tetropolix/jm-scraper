from sqlalchemy.orm import configure_mappers, relationship
from app.extensions import db

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


class Profile(db.Model):
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True)
    birth_date = db.Column(db.DateTime, nullable=True, default=None)
    avatar_uri = db.Column(db.String(256), nullable=True, default=None)
    genders = relationship(
        "Gender", secondary=profile_gender, lazy="subquery", backref="profiles"
    )
    products = relationship(
        "Product", secondary=profile_product, lazy="subquery", backref="prof    "
    )


configure_mappers()
