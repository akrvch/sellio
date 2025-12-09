import sqlalchemy as sa

from sellio.graph.enums import SortOrder
from sellio.models.product import Product


def product_sort_order_to_sqlalchemy(sort_order: SortOrder) -> sa.Column:
    match sort_order:
        case SortOrder.PRICE_ASC:
            return Product.price
        case SortOrder.PRICE_DESC:
            return Product.price.desc()
    raise ValueError(f"Invalid sort order: {sort_order}")
