from datetime import datetime
from enum import Enum
from typing import NamedTuple

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from sellio.lib.enum import SqlAlEnumDecorator
from sellio.models import Base


class OrderStatusEnumValue(NamedTuple):
    title: str


class OrderStatus(Enum):
    new = OrderStatusEnumValue(title="Нове")
    in_progress = OrderStatusEnumValue(title="Прийнято")
    completed = OrderStatusEnumValue(title="Виконано")
    cancelled = OrderStatusEnumValue(title="Скасовано")


class Order(Base):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        index=True,
        unique=True,
    )
    from_user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id"), index=True, unique=False, nullable=False
    )
    from_company_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("company.id"),
        index=True,
        unique=False,
        nullable=False,
    )
    from_first_name: Mapped[str] = mapped_column(
        String(length=50), nullable=False
    )
    from_second_name: Mapped[str] = mapped_column(
        String(length=50), nullable=False
    )
    from_last_name: Mapped[str] = mapped_column(
        String(length=50), nullable=False
    )
    from_email: Mapped[str] = mapped_column(String(length=120), nullable=False)
    from_phone: Mapped[str] = mapped_column(String(length=20), nullable=False)
    cart_id: Mapped[int] = mapped_column(
        Integer, index=True, unique=False, nullable=False
    )
    payment_option_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("payment_option.id"),
        index=False,
        unique=False,
        nullable=False,
    )
    delivery_option_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("delivery_option.id"),
        index=False,
        unique=False,
        nullable=False,
    )
    status: Mapped[OrderStatus] = mapped_column(SqlAlEnumDecorator(OrderStatus))
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    date_created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    date_updated: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )
