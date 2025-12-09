from hiku.graph import Link
from hiku.graph import Option
from hiku.types import EnumRef
from hiku.types import Integer
from hiku.types import Optional
from hiku.types import String
from hiku.types import TypeRef

from sellio.graph.listings.category.resolvers import resolve_category_listing

CategoryListingLink = Link(
    "categoryListing",
    Optional[TypeRef["CategoryListing"]],
    resolve_category_listing,
    requires=None,
    options=[
        Option("alias", String),
        Option("limit", Integer),
        Option("offset", Integer),
        Option("sort", EnumRef["SortOrder"]),
    ],
)
