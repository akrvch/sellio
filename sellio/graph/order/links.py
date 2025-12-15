from hiku.graph import Link
from hiku.graph import Option
from hiku.types import Integer
from hiku.types import Optional
from hiku.types import Sequence
from hiku.types import String
from hiku.types import TypeRef

from sellio.graph.order.resolvers import link_order_details
from sellio.graph.order.resolvers import link_order_list
from sellio.graph.order.resolvers import mutation_create_order
from sellio.graph.order.resolvers import query_checkout
from sellio.graph.order.resolvers import query_thank_you_page

# Query Links
OrderListLink = Link(
    "orderList",
    Sequence[TypeRef["Order"]],
    link_order_list,
    options=[
        Option("limit", Integer),
        Option("offset", Integer),
    ],
    requires=None,
)

OrderDetailsLink = Link(
    "orderDetails",
    Optional[TypeRef["Order"]],
    link_order_details,
    options=[
        Option("id", Integer),
    ],
    requires=None,
)

CheckoutLink = Link(
    "checkout",
    Optional[TypeRef["CheckoutPage"]],
    query_checkout,
    options=[
        Option("cartId", Integer),
    ],
    requires=None,
)

ThankYouPageLink = Link(
    "thankYouPage",
    Optional[TypeRef["ThankYouPage"]],
    query_thank_you_page,
    options=[
        Option("orderId", Integer),
    ],
    requires=None,
)

# Mutation Links
CreateOrderLink = Link(
    "createOrder",
    TypeRef["CreateOrderResponse"],
    mutation_create_order,
    options=[
        Option("cartId", Integer),
        Option("paymentOptionId", Integer),
        Option("deliveryOptionId", Integer),
        Option("comment", Optional[String]),
        Option("fromFirstName", String),
        Option("fromSecondName", String),
        Option("fromLastName", String),
        Option("fromPhone", String),
        Option("fromEmail", String),
        Option("city", Optional[String]),
        Option("warehouse", Optional[String]),
        Option("fullDeliveryAddress", Optional[String]),
    ],
    requires=None,
)
