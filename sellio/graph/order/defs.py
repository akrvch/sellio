from dataclasses import dataclass
from datetime import datetime

from hiku.expr.core import define
from hiku.scalar import Date
from hiku.types import Any, Boolean, Integer, Sequence
from hiku.types import Record
from httpx import Proxy

from sellio.graph.order.types import OrderDeliveryOptionContext, OrderPaymentOptionContext
from sellio.models.order import OrderStatus


@dataclass(frozen=True)
class GraphOrderStatus:
    key: str
    title: str


@define(Any)
def get_order_status(status: OrderStatus) -> GraphOrderStatus:
    return GraphOrderStatus(
        key=status.name,
        title=status.value.title,
    )


@define(
    Record[
        {
            "date_created": Date,
        }
    ]
)
def get_order_date_created(order_with_date_proxy: Proxy) -> str:
    date_created = order_with_date_proxy.date_created
    return date_created.strftime("%Y-%m-%d %H:%M:%S")


@define(
    Record[
        {
            "id": Integer,
            "type": Any,
            "active": Boolean,
        }
    ]
)
def get_order_delivery_options_context(
    opt: Proxy,
) -> list[OrderDeliveryOptionContext]:
    return OrderDeliveryOptionContext(
        id=opt.id, 
        type=opt.type.name, 
        name=opt.type.value.title,
    )


@define(
    Record[
        {
            "id": Integer,
            "type": Any,
            "active": Boolean,
        }
    ]
)
def get_order_payment_options_context(
    opt: Proxy,
) -> list[OrderPaymentOptionContext]:
    return OrderPaymentOptionContext(
        id=opt.id, 
        type=opt.type.name, 
        name=opt.type.value.title,
    )

