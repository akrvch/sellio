from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from sellio.models import Base


class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        index=True,
        unique=True,
    )
    name: Mapped[str] = mapped_column(String(length=120))
    description: Mapped[str] = mapped_column(Text)
    parent_category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("category.id"), index=True, unique=False
    )
    is_adult: Mapped[bool] = mapped_column(Boolean, default=False)
