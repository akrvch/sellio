from datetime import date
from decimal import Decimal


def discount_is_active(start_at: date, end_at: date) -> bool:
    today = date.today()
    return today >= start_at and today <= end_at


def get_discounted_proudct_pirce(
    price: Decimal, discount_percent: int
) -> Decimal:
    return price * (1 - discount_percent / 100)
