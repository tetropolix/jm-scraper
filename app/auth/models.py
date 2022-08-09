from sqlalchemy.orm import configure_mappers
from app.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="User")


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False, index=True)
    username = db.Column(db.String(128), nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    email_activated = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(
        db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now()
    )

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password_to_verify):
        return check_password_hash(self.password_hash, password_to_verify)

    def __repr__(self):
        return "<User with email <%s>>" % (self.email)

    @classmethod
    def query_by_email(cls: Type[T], email: str) -> Optional[T]:
        return cls.query.filter_by(email=email).first()

    def save(self) -> int:
        db.session.add(self)
        db.session.commit()
        return self.id

configure_mappers()