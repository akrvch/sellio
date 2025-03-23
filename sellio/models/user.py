from models import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from sellio.services.hash import PasswordHasher


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, index=True
    )
    first_name: Mapped[str] = mapped_column()
    second_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(index=True, unique=True)
    phone: Mapped[str] = mapped_column(index=True, unique=True)
    hashed_password: Mapped[str]
    is_superuser: Mapped[bool] = mapped_column(default=False)

    @staticmethod
    def generate_password_hash(password: str) -> str:
        return PasswordHasher.hash(password)

    def is_password_correct(self, password: str) -> bool:
        return PasswordHasher.verify(password, self.hashed_password)
