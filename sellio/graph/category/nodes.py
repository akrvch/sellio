from hiku.expr.core import S
from hiku.graph import Field
from hiku.graph import Link
from hiku.graph import Node
from hiku.types import Any, Boolean
from hiku.types import Integer
from hiku.types import Sequence
from hiku.types import String
from hiku.types import TypeRef

from sellio.graph import direct_link
from sellio.graph.category.resolvers import map_categories

CategoryNode = Node(
    "Category",
    [
        Field("id", Integer, map_categories),
        Field("name", String, map_categories),
        Field("alias", String, map_categories),
        Field("isAdult", Boolean, map_categories),
        Field("description", String, map_categories),
        Field("_path", Sequence[Any], map_categories),
        Field("_child_categories", Sequence[Any], map_categories),
        Link(
            "childCategories",
            Sequence[TypeRef["Category"]],
            direct_link,
            requires="_child_categories",
        ),
        Link(
            "path",
            Sequence[TypeRef["Category"]],
            direct_link,
            requires="_path",
        ),
    ],
)
