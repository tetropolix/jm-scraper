from sqlalchemy.orm import configure_mappers, relationship, backref
from app.extensions import db
from app.auth.models import User
from app.products.models import Gender, Product

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
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = relationship("User", backref=backref("profile", uselist=False))
    genders = relationship(
        "Gender", secondary=profile_gender, lazy="subquery", backref="profiles"
    )
    products = relationship(
        "Product", secondary=profile_product, lazy="subquery", backref="prof    "
    )

    @classmethod
    def query_by_id(cls, id: int):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def query_by_user_id(cls, user_id: int):
        return cls.query.filter_by(id=id).first()


configure_mappers()
