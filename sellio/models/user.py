from sqlalchemy import Boolean
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from sellio.models import Base
from sellio.services.hash import PasswordHasher


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, index=True
    )
    first_name: Mapped[str] = mapped_column(String(length=50))
    second_name: Mapped[str] = mapped_column(String(length=50))
    last_name: Mapped[str] = mapped_column(String(length=50))
    email: Mapped[str] = mapped_column(
        String(length=120), index=True, unique=True
    )
    phone: Mapped[str] = mapped_column(
        String(length=20), index=True, unique=True
    )
    hashed_password: Mapped[str] = mapped_column(String(length=200))
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

    @staticmethod
    def generate_password_hash(password: str) -> str:
        return PasswordHasher.hash(password)

    def is_password_correct(self, password: str) -> bool:
        return PasswordHasher.verify(password, self.hashed_password)
