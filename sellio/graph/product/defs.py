from hiku.expr.core import define
from hiku.result import Proxy
from hiku.types import Any
from hiku.types import Boolean
from hiku.types import Integer
from hiku.types import Record
from hiku.types import Sequence

from sellio.graph.product.types import ProductDeliveryOptionContext
from sellio.graph.product.types import ProductPaymentOptionContext


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
