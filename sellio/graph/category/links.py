from hiku.graph import Link
from hiku.graph import Option
from hiku.types import Optional
from hiku.types import String
from hiku.types import TypeRef

from sellio.graph.category.resolvers import link_category

CategoryLink = Link(
    "category",
    Optional[TypeRef["Category"]],
    link_category,
    requires=None,
    options=[
        Option("alias", String),
    ],
)
