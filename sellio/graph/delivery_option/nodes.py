from hiku.graph import Field
from hiku.graph import Node
from hiku.types import Integer
from hiku.types import String

from sellio.graph import UniversalMapper

delivery_option_mapper = UniversalMapper("DeliveryOption")


DeliveryOptionNode = Node(
    "DeliveryOption",
    [
        Field("id", Integer, delivery_option_mapper),
        Field("name", String, delivery_option_mapper),
        Field("type", String, delivery_option_mapper),
    ],
)
