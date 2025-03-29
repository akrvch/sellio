from hiku.expr.core import S
from hiku.graph import Field
from hiku.graph import Link
from hiku.graph import Node
from hiku.types import Integer
from hiku.types import Sequence
from hiku.types import String
from hiku.types import TypeRef

from sellio.db_graph import product_sg
from sellio.graph import direct_link
from sellio.graph.product.defs import get_product_delivery_options_contexts
from sellio.graph.product.defs import get_product_payment_options_contexts

ProductNode = Node(
    "Product",
    [
        Field("id", Integer, product_sg),
        Field("name", String, product_sg.c(S.this.name)),
        Field("description", String, product_sg.c(S.this.name)),
        Field("price", String, product_sg.c(S.this.name)),
        Field("categoryId", String, product_sg.c(S.this.category_id)),
        Field("companyId", String, product_sg.c(S.this.company_id)),
        Field(
            "_delivery_options_context",
            String,
            product_sg.c(
                get_product_delivery_options_contexts(
                    S.this.company.delivery_options
                )
            ),
        ),
        Field(
            "_payment_options_context",
            String,
            product_sg.c(
                get_product_payment_options_contexts(
                    S.this.company.payment_options
                )
            ),
        ),
        Link(
            "company",
            TypeRef["Company"],
            direct_link,
            requires="companyId",
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
