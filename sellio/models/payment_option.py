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


class PaymentOptionEnumValue(NamedTuple):
    title: str
    description: str


class PaymentOptionType(Enum):
    card = PaymentOptionEnumValue(title="Оплата картою", description="")
    bank_account = PaymentOptionEnumValue(
        title="Оплата за реквізитами", description=""
    )
    cash_on_delivery = PaymentOptionEnumValue(
        title="Післяплата", description=""
    )


class PaymentOption(Base):
    __tablename__ = "payment_option"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        index=True,
        unique=True,
    )
    company_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("company.id"), index=True, unique=False
    )
    type: Mapped[PaymentOptionType] = mapped_column(
        SqlAlEnumDecorator(PaymentOptionType)
    )
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    __table_args__ = (
        UniqueConstraint(
            "company_id", "type", name="ix_company_id_payment_option_type"
        ),
    )
