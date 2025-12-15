from hiku.expr.core import S
from hiku.graph import Field
from hiku.graph import Link
from hiku.graph import Node
from hiku.types import Integer
from hiku.types import Sequence
from hiku.types import Any
from hiku.types import String
from hiku.types import TypeRef

from sellio.db_graph import company_sg
from sellio.graph import direct_link
from sellio.graph.company.defs import get_company_delivery_options_contexts
from sellio.graph.company.defs import get_company_payment_options_contexts

CompanyNode = Node(
    "Company",
    [
        Field("id", Integer, company_sg),
        Field("name", String, company_sg.c(S.this.name)),
        Field("email", String, company_sg.c(S.this.email)),
        Field("phone", String, company_sg.c(S.this.phone)),
        Field(
            "_delivery_options_context",
            Any,
            company_sg.c(
                get_company_delivery_options_contexts(S.this.delivery_options)
            ),
        ),
        Field(
            "_payment_options_context",
            Any,
            company_sg.c(
                get_company_payment_options_contexts(S.this.payment_options)
            ),
        ),
        Link(
            "deliveryOptions",
            Sequence[TypeRef["DeliveryOption"]],
            direct_link,
            requires="_delivery_options_context",
        ),
        Link(
            "paymentOptions",
            Sequence[TypeRef["PaymentOption"]],
            direct_link,
            requires="_payment_options_context",
        ),
    ],
)
