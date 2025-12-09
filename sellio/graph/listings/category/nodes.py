from hiku.graph import Field
from hiku.graph import Link
from hiku.graph import Node
from hiku.types import Any
from hiku.types import Integer
from hiku.types import Optional
from hiku.types import TypeRef

from sellio.graph import UniversalMapper, direct_link, maybe_direct_link

category_listing_mapper = UniversalMapper("CategoryListing")


CategoryListingNode = Node(
    "CategoryListing",
    [
        Field("_category_id", Integer, category_listing_mapper),
        Field("_page", Any, category_listing_mapper),
        Link(
            "category",
            TypeRef["Category"],
            direct_link,
            requires="_category_id",
        ),
        Link(
            "page",
            Optional[TypeRef["ListingPage"]],
            maybe_direct_link,
            requires="_page",
        ),
    ],
)
