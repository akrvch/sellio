from hiku.expr.core import S
from hiku.graph import Field
from hiku.graph import Link
from hiku.graph import Node
from hiku.types import Boolean
from hiku.types import Integer
from hiku.types import Sequence
from hiku.types import String
from hiku.types import TypeRef

from sellio.db_graph import category_sg
from sellio.graph import direct_link

CategoryNode = Node(
    "Category",
    [
        Field("id", Integer, category_sg),
        Field("name", String, category_sg.c(S.this.name)),
        Field("isAdult", Boolean, category_sg.c(S.this.is_adult)),
        Field(
            "_child_category_ids",
            Sequence[Integer],
            category_sg.c(S.this.child_category_ids),
        ),
        Link(
            "childCategories",
            Sequence[TypeRef["Category"]],
            direct_link,
            requires="_child_category_ids",
        ),
    ],
)
