from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from sellio.models import Base


class Company(Base):
    __tablename__ = "company"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        index=True,
        unique=True,
    )
    name: Mapped[str] = mapped_column(String(length=120))
    owner_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id"), index=True, unique=False
    )
    email: Mapped[str] = mapped_column(String(length=120))
    phone: Mapped[str] = mapped_column(String(length=20))
