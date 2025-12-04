from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from sellio.models import Base


class ProductGroup(Base):
    __tablename__ = "product_group"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        index=True,
        unique=True,
    )
    name: Mapped[str] = mapped_column(String(length=120))
