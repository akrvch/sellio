from datetime import date

from sqlalchemy import CheckConstraint
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from sellio.models import Base


class ProductDiscount(Base):
    __tablename__ = "product_discount"

    __table_args__ = (
        CheckConstraint(
            "percent >= 1 AND percent <= 99", name="check_percent_range"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        index=True,
        unique=True,
    )
    percent: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    start_at: Mapped[date] = mapped_column(Date)
    end_at: Mapped[date] = mapped_column(Date)
    product_group_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("product_group.id"), index=True, unique=False
    )
