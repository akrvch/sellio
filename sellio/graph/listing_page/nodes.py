from hiku.graph import Field, Link
from hiku.graph import Node
from hiku.types import Integer
from hiku.types import Sequence
from hiku.types import TypeRef

from sellio.graph import UniversalMapper
from sellio.graph import direct_link

listing_page_mapper = UniversalMapper("ListingPage")


ListingPageNode = Node(
    "ListingPage",
    [
        Field("_product_ids", Sequence[Integer], listing_page_mapper),
        Link(
            "products",
            Sequence[TypeRef["Product"]],
            direct_link,
            requires="_product_ids",
        ),
    ],
)
