from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from sellio.models import Base


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        index=True,
        unique=True,
    )
    name: Mapped[str] = mapped_column(String(length=120))
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    company_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("company.id"), index=True, unique=False
    )
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("category.id"), index=True, unique=False
    )
    product_group_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("product_group.id"),
        index=True,
        unique=False,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
