from hiku.expr.core import S
from hiku.graph import Field
from hiku.graph import Link
from hiku.graph import Node
from hiku.types import Any
from hiku.types import Boolean
from hiku.types import Integer
from hiku.types import Optional
from hiku.types import String
from hiku.types import TypeRef

from sellio.db_graph import order_sg
from sellio.graph import UniversalMapper
from sellio.graph import direct_link
from sellio.graph.order.defs import get_order_delivery_options_context, get_order_payment_options_context, get_order_status, get_order_date_created
from sellio.graph.order.resolvers import link_order_cart
from sellio.graph.order.resolvers import link_order_delivery_info

order_status_mapper = UniversalMapper("OrderStatus")
checkout_page_mapper = UniversalMapper("CheckoutPage")
thank_you_page_mapper = UniversalMapper("ThankYouPage")
create_order_response_mapper = UniversalMapper("CreateOrderResponse")


OrderStatusNode = Node(
    "OrderStatus",
    [
        Field("key", Integer, order_status_mapper),
        Field("title", String, order_status_mapper),
    ],
)


OrderNode = Node(
    "Order",
    [
        Field("id", Integer, order_sg),
        Field("fromFirstName", String, order_sg.c(S.this.from_first_name)),
        Field("fromSecondName", String, order_sg.c(S.this.from_second_name)),
        Field("fromLastName", String, order_sg.c(S.this.from_last_name)),
        Field("fromEmail", String, order_sg.c(S.this.from_email)),
        Field("fromPhone", String, order_sg.c(S.this.from_phone)),
        Field(
            "_status",
            String,
            order_sg.c(get_order_status(S.this.status)),
        ),
        Link("status", TypeRef["OrderStatus"], direct_link, requires="_status"),
        Field("comment", Optional[String], order_sg.c(S.this.comment)),
        Field("dateCreated", String, order_sg.c(get_order_date_created(S.this))),
        Field("_cart_id", Integer, order_sg.c(S.this.cart_id)),
        Field("_company_id", Integer, order_sg.c(S.this.from_company_id)),
        Field(
            "_payment_option_context", Integer, order_sg.c(get_order_payment_options_context(S.this.payment_option))
        ),
        Field(
            "_delivery_option_context",
            Integer, order_sg.c(get_order_delivery_options_context(S.this.delivery_option)),
        ),
        Field("_delivery_info_id", Any, order_sg.c(S.this.delivery_info_id)),
        Link("cart", TypeRef["Cart"], link_order_cart, requires="_cart_id"),
        Link(
            "paymentOption",
            TypeRef["PaymentOption"],
            direct_link,
            requires="_payment_option_context",
        ),
        Link(
            "deliveryOption",
            TypeRef["DeliveryOption"],
            direct_link,
            requires="_delivery_option_context",
        ),
        Link(
            "company", TypeRef["Company"], direct_link, requires="_company_id"
        ),
        Link(
            "deliveryInfo",
            Optional[TypeRef["DeliveryInfo"]],
            link_order_delivery_info,
            requires="_delivery_info_id",
        ),
    ],
)


CheckoutPageNode = Node(
    "CheckoutPage",
    [
        Field("_cart", Any, checkout_page_mapper),
        Link(
            "cart",
            TypeRef["Cart"],
            direct_link,
            requires="_cart",
        ),
    ],
)

ThankYouPageNode = Node(
    "ThankYouPage",
    [
        Field("_order_id", Any, thank_you_page_mapper),
        Link(
            "order",
            TypeRef["Order"],
            direct_link,
            requires="_order_id",
        ),
    ],
)

CreateOrderResponseNode = Node(
    "CreateOrderResponse",
    [
        Field("success", Boolean, create_order_response_mapper),
        Field("message", String, create_order_response_mapper),
        Field("orderId", Optional[Integer], create_order_response_mapper),
    ],
)
