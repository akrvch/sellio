from hiku.expr.core import S
from hiku.graph import Field
from hiku.graph import Link
from hiku.graph import Node
from hiku.types import Integer
from hiku.types import Optional
from hiku.types import String
from hiku.types import TypeRef

from sellio.db_graph import delivery_info_sg
from sellio.graph import UniversalMapper
from sellio.graph import direct_link
from sellio.graph.delivery_info.defs import get_delivery_info_status

delivery_info_status_mapper = UniversalMapper("DeliveryInfoStatus")


DeliveryInfoStatusNode = Node(
    "DeliveryInfoStatus",
    [
        Field("key", Integer, delivery_info_status_mapper),
        Field("title", String, delivery_info_status_mapper),
    ],
)


DeliveryInfoNode = Node(
    "DeliveryInfo",
    [
        Field("id", Integer, delivery_info_sg),
        Field(
            "_status",
            String,
            delivery_info_sg.c(get_delivery_info_status(S.this.status)),
        ),
        Link(
            "status",
            TypeRef["DeliveryInfoStatus"],
            direct_link,
            requires="_status",
        ),
        Field(
            "declarationId",
            Optional[String],
            delivery_info_sg.c(S.this.declaration_id),
        ),
        Field("city", Optional[String], delivery_info_sg.c(S.this.city)),
        Field("warehouse", Optional[String], delivery_info_sg.c(S.this.warehouse)),
        Field(
            "fullDeliveryAddress",
            Optional[String],
            delivery_info_sg.c(S.this.full_delivery_address),
        ),
    ],
)
