from hiku.expr.core import define
from hiku.result import Proxy
from hiku.types import Any
from hiku.types import Boolean
from hiku.types import Integer
from hiku.types import Record
from hiku.types import Sequence

from sellio.graph.company.types import CompanyDeliveryOptionContext
from sellio.graph.company.types import CompanyPaymentOptionContext


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
def get_company_delivery_options_contexts(
    opts: list[Proxy],
) -> list[CompanyDeliveryOptionContext]:
    return [
        CompanyDeliveryOptionContext(
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
def get_company_payment_options_contexts(
    opts: list[Proxy],
) -> list[CompanyPaymentOptionContext]:
    return [
        CompanyPaymentOptionContext(
            id=opt.id, type=opt.type.name, name=opt.type.value.title
        )
        for opt in opts
    ]

