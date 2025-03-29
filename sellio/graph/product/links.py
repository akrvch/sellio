from hiku.graph import Link
from hiku.graph import Option
from hiku.types import Integer
from hiku.types import Sequence
from hiku.types import TypeRef

from sellio.graph.product.resolvers import link_products_list

ProductListLink = Link(
    "productList",
    Sequence[TypeRef["Product"]],
    link_products_list,
    options=[
        Option("productIds", Sequence[Integer]),
    ],
    requires=None,
)
