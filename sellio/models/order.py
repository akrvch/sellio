from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from sellio.models import Base


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
