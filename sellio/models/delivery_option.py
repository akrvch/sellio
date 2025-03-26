from enum import Enum
from typing import NamedTuple

from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from sellio.lib.enum import SqlAlEnumDecorator
from sellio.models import Base


class DeliveryOptionEnumValue(NamedTuple):
    name: str
    description: str


class DeliveryOptionType(Enum):
    nova_poshta = DeliveryOptionEnumValue(name="Нова Пошта", description="")
    ukrposhta = DeliveryOptionEnumValue(name="УкрПошта", description="")
    meest = DeliveryOptionEnumValue(name="Meest", description="")
    pickup = DeliveryOptionEnumValue(name="Самовивіз", description="")


class DeliveryOption(Base):
    __tablename__ = "delivery_option"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        index=True,
        unique=True,
    )
    company_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("company.id"), index=True, unique=False
    )
    type: Mapped[DeliveryOptionType] = mapped_column(
        SqlAlEnumDecorator(DeliveryOptionType)
    )
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    __table_args__ = (
        UniqueConstraint(
            "company_id", "type", name="ix_company_id_delivery_option_type"
        ),
    )
