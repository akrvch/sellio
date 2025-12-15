from datetime import datetime
from enum import Enum
from typing import NamedTuple

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from sellio.lib.enum import SqlAlEnumDecorator
from sellio.models import Base


class DeliveryStatusEnumValue(NamedTuple):
    title: str


class DeliveryStatus(Enum):
    init = DeliveryStatusEnumValue(title="Ініційовано")
    created = DeliveryStatusEnumValue(title="Створено")
    sent = DeliveryStatusEnumValue(title="Відправлено")
    delivered = DeliveryStatusEnumValue(title="Доставлено")
    cancelled = DeliveryStatusEnumValue(title="Скасовано")
    completed = DeliveryStatusEnumValue(title="Завершено")
    returned = DeliveryStatusEnumValue(title="Повернено")


class DeliveryInfo(Base):
    __tablename__ = "delivery_info"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        index=True,
        unique=True,
    )
    order_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("order.id"), index=True, unique=True, nullable=False
    )
    status: Mapped[DeliveryStatus] = mapped_column(
        SqlAlEnumDecorator(DeliveryStatus), nullable=False
    )
    declaration_id: Mapped[str | None] = mapped_column(
        String(length=100), nullable=True
    )
    city: Mapped[str | None] = mapped_column(String(length=100), nullable=True)
    warehouse: Mapped[str | None] = mapped_column(
        String(length=100), nullable=True
    )
    full_delivery_address: Mapped[str | None] = mapped_column(
        String(length=500), nullable=True
    )
    date_created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    date_updated: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )
