"""Cart GraphQL nodes."""

from hiku.graph import Field
from hiku.graph import Link
from hiku.graph import Node
from hiku.types import Any
from hiku.types import Boolean
from hiku.types import Integer
from hiku.types import Optional
from hiku.types import Sequence
from hiku.types import String
from hiku.types import TypeRef

from sellio.graph import UniversalMapper
from sellio.graph import direct_link
from sellio.graph import maybe_direct_link

# Mappers
cart_item_mapper = UniversalMapper("CartItem")
cart_mapper = UniversalMapper("Cart")
add_item_mapper = UniversalMapper("AddItemResponse")
update_quantity_mapper = UniversalMapper("UpdateQuantityResponse")
remove_item_mapper = UniversalMapper("RemoveItemResponse")

# Cart Item Node
CartItemNode = Node(
    "CartItem",
    [
        Field("productId", Integer, cart_item_mapper),
        Field("name", String, cart_item_mapper),
        Field("price", String, cart_item_mapper),
        Field("quantity", Integer, cart_item_mapper),
        Link(
            "product",
            Optional[TypeRef["Product"]],
            maybe_direct_link,
            requires="productId",
        ),
    ],
)

# Cart Node
CartNode = Node(
    "Cart",
    [
        Field("id", Integer, cart_mapper),
        Field("companyId", Integer, cart_mapper),
        Field("userId", Optional[Integer], cart_mapper),
        Field("cookie", Optional[String], cart_mapper),
        Field("status", Integer, cart_mapper),
        Field("createdAt", String, cart_mapper),
        Field("totalAmount", String, cart_mapper),
        Field("_items", Any, cart_mapper),
        Link(
            "items",
            Sequence[TypeRef["CartItem"]],
            direct_link,
            requires="_items",
        ),
        Link(
            "company",
            TypeRef["Company"],
            direct_link,
            requires="companyId",
        ),
    ],
)

# Response Nodes
AddItemNode = Node(
    "AddItemResponse",
    [
        Field("success", Boolean, add_item_mapper),
        Field("message", String, add_item_mapper),
        Field("_cart", Any, add_item_mapper),
        Link(
            "cart",
            Optional[TypeRef["Cart"]],
            maybe_direct_link,
            requires="_cart",
        ),
    ],
)

UpdateQuantityNode = Node(
    "UpdateQuantityResponse",
    [
        Field("success", Boolean, update_quantity_mapper),
        Field("message", String, update_quantity_mapper),
        Field("_cart", Any, update_quantity_mapper),
        Link(
            "cart",
            Optional[TypeRef["Cart"]],
            maybe_direct_link,
            requires="_cart",
        ),
    ],
)

RemoveItemNode = Node(
    "RemoveItemResponse",
    [
        Field("success", Boolean, remove_item_mapper),
        Field("message", String, remove_item_mapper),
        Field("_cart", Any, remove_item_mapper),
        Link(
            "cart",
            Optional[TypeRef["Cart"]],
            maybe_direct_link,
            requires="_cart",
        ),
    ],
)
