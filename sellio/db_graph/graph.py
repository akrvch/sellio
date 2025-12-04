from hiku.graph import Field
from hiku.graph import Graph
from hiku.graph import Link
from hiku.graph import Node
from hiku.scalar import Date
from hiku.sources.sqlalchemy_async import FieldsQuery
from hiku.types import Any
from hiku.types import Boolean
from hiku.types import Integer
from hiku.types import Optional
from hiku.types import Sequence
from hiku.types import String
from hiku.types import TypeRef

from sellio.db_graph.resolvers.category import resolve_child_category_ids
from sellio.db_graph.resolvers.company import link_company_delivery_options
from sellio.db_graph.resolvers.company import link_company_payment_options
from sellio.graph import direct_link
from sellio.graph import maybe_direct_link
from sellio.models import Category
from sellio.models import Company
from sellio.models import DeliveryOption
from sellio.models import Order
from sellio.models import PaymentOption
from sellio.models import Product
from sellio.models import ProductDiscount

product_query = FieldsQuery("db.session_async", Product.__table__)
company_query = FieldsQuery("db.session_async", Company.__table__)
category_query = FieldsQuery("db.session_async", Category.__table__)
delivery_option_query = FieldsQuery(
    "db.session_async", DeliveryOption.__table__
)
payment_option_query = FieldsQuery("db.session_async", PaymentOption.__table__)
order_query = FieldsQuery("db.session_async", Order.__table__)
product_discount_query = FieldsQuery(
    "db.session_async", ProductDiscount.__table__
)


_GRAPH = Graph(
    [
        Node(
            "product",
            [
                Field("id", Integer, product_query),
                Field("name", String, product_query),
                Field("description", String, product_query),
                Field("price", String, product_query),
                Field("company_id", Integer, product_query),
                Field("category_id", Integer, product_query),
                Field("product_group_id", Optional[Integer], product_query),
                Link(
                    "product_discount",
                    Optional[TypeRef["product_discount"]],
                    maybe_direct_link,
                    requires="product_group_id",
                ),
                Link(
                    "company",
                    TypeRef["company"],
                    direct_link,
                    requires="company_id",
                ),
            ],
        ),
        Node(
            "product_discount",
            [
                Field("id", Integer, product_discount_query),
                Field("percent", Integer, product_discount_query),
                Field("start_at", Date, product_discount_query),
                Field("end_at", Date, product_discount_query),
            ],
        ),
        Node(
            "company",
            [
                Field("id", Integer, company_query),
                Field("name", String, company_query),
                Field("email", String, company_query),
                Field("phone", String, company_query),
                Link(
                    "payment_options",
                    Sequence[TypeRef["payment_option"]],
                    link_company_payment_options,
                    requires="id",
                ),
                Link(
                    "delivery_options",
                    Sequence[TypeRef["delivery_option"]],
                    link_company_delivery_options,
                    requires="id",
                ),
            ],
        ),
        Node(
            "category",
            [
                Field("id", Integer, category_query),
                Field("name", String, category_query),
                Field("description", String, category_query),
                Field("is_adult", Boolean, category_query),
                Field(
                    "child_category_ids",
                    Sequence[Integer],
                    resolve_child_category_ids,
                ),
            ],
        ),
        Node(
            "delivery_option",
            [
                Field("id", Integer, delivery_option_query),
                Field("type", Any, delivery_option_query),
                Field("active", Boolean, delivery_option_query),
            ],
        ),
        Node(
            "payment_option",
            [
                Field("id", Integer, payment_option_query),
                Field("type", Any, payment_option_query),
                Field("active", Boolean, payment_option_query),
            ],
        ),
        Node(
            "order",
            [
                Field("id", Integer, order_query),
                Field("from_user_id", Integer, order_query),
                Field("from_company_id", Integer, order_query),
                Field("from_first_name", String, order_query),
                Field("from_second_name", String, order_query),
                Field("from_last_name", String, order_query),
                Field("from_email", String, order_query),
                Field("from_phone", String, order_query),
                Field("cart_id", Integer, order_query),
                Field("payment_option_id", Integer, order_query),
                Field("delivery_option_id", Integer, order_query),
            ],
        ),
    ],
    scalars=[Date],
)
