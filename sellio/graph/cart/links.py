"""Cart GraphQL links."""

from hiku.graph import Link
from hiku.graph import Option
from hiku.types import Integer
from hiku.types import Sequence
from hiku.types import TypeRef

from sellio.graph.cart.resolvers import mutation_add_item
from sellio.graph.cart.resolvers import mutation_remove_item
from sellio.graph.cart.resolvers import mutation_update_quantity
from sellio.graph.cart.resolvers import query_user_carts

# Query Links
UserCartsLink = Link(
    "userCarts",
    Sequence[TypeRef["Cart"]],
    query_user_carts,
    options=[],
    requires=None,
)

# Mutation Links
AddItemLink = Link(
    "addItemToCart",
    TypeRef["AddItemResponse"],
    mutation_add_item,
    options=[
        Option("productId", Integer),
    ],
    requires=None,
)

UpdateQuantityLink = Link(
    "updateCartItemQuantity",
    TypeRef["UpdateQuantityResponse"],
    mutation_update_quantity,
    options=[
        Option("productId", Integer),
        Option("quantity", Integer),
    ],
    requires=None,
)

RemoveItemLink = Link(
    "removeItemFromCart",
    TypeRef["RemoveItemResponse"],
    mutation_remove_item,
    options=[
        Option("productId", Integer),
    ],
    requires=None,
)
