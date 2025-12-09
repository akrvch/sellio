from decimal import Decimal

from hiku.expr.core import define
from hiku.result import Proxy
from hiku.scalar import Date
from hiku.types import Any
from hiku.types import Boolean
from hiku.types import Integer
from hiku.types import Optional
from hiku.types import Record
from hiku.types import Sequence
from hiku.types import String

from sellio import url
from sellio.graph.product.types import ProductDeliveryOptionContext
from sellio.graph.product.types import ProductPaymentOptionContext
from sellio.lib.product import discount_is_active
from sellio.lib.product import get_discounted_proudct_pirce


@define(
    Sequence[
        Record[
            {
                "id": Integer,
                "type": Any,
                "active": Boolean,
            }
        ]
    ]
)
def get_product_delivery_options_contexts(
    opts: list[Proxy],
) -> list[ProductDeliveryOptionContext]:
    return [
        ProductDeliveryOptionContext(
            id=opt.id, type=opt.type.name, name=opt.type.value.title
        )
        for opt in opts
    ]


@define(
    Sequence[
        Record[
            {
                "id": Integer,
                "type": Any,
                "active": Boolean,
            }
        ]
    ]
)
def get_product_payment_options_contexts(
    opts: list[Proxy],
) -> list[ProductPaymentOptionContext]:
    return [
        ProductPaymentOptionContext(
            id=opt.id, type=opt.type.name, name=opt.type.value.title
        )
        for opt in opts
    ]


@define(
    Optional[
        Record[
            {
                "percent": Any,
                "start_at": Date,
                "end_at": Date,
            }
        ]
    ],
)
def get_discount_percent(product_discount: Proxy | None) -> int | None:
    if not product_discount or not discount_is_active(
        product_discount.start_at, product_discount.end_at
    ):
        return None
    return product_discount.percent


@define(
    String,
    Optional[
        Record[
            {
                "percent": Any,
                "start_at": Date,
                "end_at": Date,
            }
        ]
    ],
)
def calculate_discounted_price(
    product_price: str, product_discount: Proxy | None
) -> str | None:
    if not product_discount or not discount_is_active(
        product_discount.start_at, product_discount.end_at
    ):
        return None
    return get_discounted_proudct_pirce(
        Decimal(product_price), product_discount.percent
    )


@define(Integer, String)
def get_product_url(product_id: int, product_name: str) -> str:
    return url.product(product_id, product_name, absolute=True)
