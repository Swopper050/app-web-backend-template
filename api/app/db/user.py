import secrets
import time

from flask_login import UserMixin
from marshmallow import Schema, fields, validate
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    hashed_password: Mapped[str] = mapped_column(String(256))

    password_reset_token: Mapped[str | None] = mapped_column(String(256), nullable=True)
    password_reset_time: Mapped[int | None] = mapped_column(nullable=True)

    def set_password(self, password: str):
        self.hashed_password = generate_password_hash(password)

    def is_correct_password(self, password: str) -> bool:
        return check_password_hash(self.hashed_password, password)

    def set_password_reset_token(self):
        token = secrets.token_urlsafe(32)
        self.password_reset_token = generate_password_hash(token)
        self.password_reset_time = int(time.time())
        return token

    def check_password_reset_token(self, reset_token: str) -> bool:
        if self.password_reset_token is None:
            return False

        return check_password_hash(self.password_reset_token, reset_token)

    def clear_password_reset_token(self):
        self.password_reset_token = None
        self.password_reset_time = None


class UserSchema(Schema):
    id = fields.Integer()
    email = fields.String(validate=validate.Length(max=100))
    is_admin = fields.Boolean()
