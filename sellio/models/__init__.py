from sqlalchemy.orm import declarative_base

Base = declarative_base()

from sellio.models.category import Category
from sellio.models.company import Company
from sellio.models.product import Product
from sellio.models.user import User
