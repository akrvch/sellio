# from sqlalchemy import ForeignKey
# from sqlalchemy import Integer
# from sqlalchemy import String
# from sqlalchemy.orm import Mapped
# from sqlalchemy.orm import mapped_column
#
# from sellio.models import Base
#
#
# class Order(Base):
#     __tablename__ = "order"
#
#     id: Mapped[int] = mapped_column(
#         primary_key=True,
#         autoincrement=True,
#         index=True,
#         unique=True,
#     )
#     from_user_id: Mapped[int] = mapped_column(
#         Integer, ForeignKey("user.id"), index=True, unique=False
#     )
#     from_company_id: Mapped[int] = mapped_column(
#         Integer, ForeignKey("company.id"), index=True, unique=False
#     )
#     from_first_name: Mapped[str] = mapped_column(String(length=50))
#     from_second_name: Mapped[str] = mapped_column(String(length=50))
#     from_last_name: Mapped[str] = mapped_column(String(length=50))
#     from_email: Mapped[str] = mapped_column(String(length=120), nullable=False)
#     from_phone: Mapped[str] = mapped_column(String(length=20))
#     cart_id: Mapped[int] = mapped_column(
#         Integer, index=True, unique=False
#     )
