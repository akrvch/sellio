from hiku.graph import Link
from hiku.types import Sequence
from hiku.types import TypeRef

from sellio.graph.menu.resolvers import link_menu

MenuLink = Link(
    "menu",
    Sequence[TypeRef["Category"]],
    link_menu,
    requires=None,
)
