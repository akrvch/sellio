from hiku.graph import Link
from hiku.types import Optional
from hiku.types import TypeRef

from sellio.graph.user.resolvers import link_current_user

CurrentUserLink = Link(
    "currentUser",
    Optional[TypeRef["User"]],
    link_current_user,
    requires=None,
)
