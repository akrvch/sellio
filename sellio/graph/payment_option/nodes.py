from hiku.graph import Field
from hiku.graph import Node
from hiku.types import Integer
from hiku.types import String

from sellio.graph import UniversalMapper

payment_option_mapper = UniversalMapper("PaymentOption")


PaymentOptionNode = Node(
    "PaymentOption",
    [
        Field("id", Integer, payment_option_mapper),
        Field("name", String, payment_option_mapper),
        Field("type", String, payment_option_mapper),
    ],
)
