from dataclasses import dataclass

from hiku.expr.core import define
from hiku.types import Any

from sellio.models.delivery_info import DeliveryStatus


@dataclass(frozen=True)
class GraphDeliveryInfoStatus:
    key: str
    title: str


@define(Any)
def get_delivery_info_status(status: DeliveryStatus) -> GraphDeliveryInfoStatus:
    return GraphDeliveryInfoStatus(
        key=status.name,
        title=status.value.title,
    )
