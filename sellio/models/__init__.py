from sqlalchemy.orm import declarative_base

Base = declarative_base()

from sellio.models.category import Category
from sellio.models.company import Company
from sellio.models.delivery_option import DeliveryOption
from sellio.models.order import Order
from sellio.models.payment_option import PaymentOption
from sellio.models.product import Product
from sellio.models.product_discount import ProductDiscount
from sellio.models.product_group import ProductGroup
from sellio.models.user import User
