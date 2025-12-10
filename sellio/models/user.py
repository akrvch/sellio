from sqlalchemy import Boolean
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from sellio.models import Base
from sellio.services.hash import password_hasher


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, index=True
    )
    phone: Mapped[str] = mapped_column(
        String(length=20), index=True, unique=True
    )
    first_name: Mapped[str | None] = mapped_column(
        String(length=50), nullable=True
    )
    second_name: Mapped[str | None] = mapped_column(
        String(length=50), nullable=True
    )
    last_name: Mapped[str | None] = mapped_column(
        String(length=50), nullable=True
    )
    email: Mapped[str | None] = mapped_column(
        String(length=120), index=True, unique=True, nullable=True
    )
    hashed_password: Mapped[str | None] = mapped_column(
        String(length=200), nullable=True
    )
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

    @property
    def is_profile_completed(self) -> bool:
        """Check if user profile is completed."""
        return bool(self.first_name and self.second_name and self.last_name)

    @staticmethod
    def generate_password_hash(password: str) -> str:
        return password_hasher.hash(password)

    def is_password_correct(self, password: str) -> bool:
        return password_hasher.verify(password, self.hashed_password)
