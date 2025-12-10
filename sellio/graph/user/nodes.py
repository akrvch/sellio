from hiku.graph import Field
from hiku.graph import Node
from hiku.types import Boolean
from hiku.types import Integer
from hiku.types import Optional
from hiku.types import String

from sellio.graph import UniversalMapper

user_mapper = UniversalMapper("UserResponse")

UserNode = Node(
    "User",
    [
        Field("id", Integer, user_mapper),
        Field("phone", String, user_mapper),
        Field("firstName", Optional[String], user_mapper),
        Field("secondName", Optional[String], user_mapper),
        Field("lastName", Optional[String], user_mapper),
        Field("email", Optional[String], user_mapper),
        Field("isProfileCompleted", Boolean, user_mapper),
        Field("isSuperuser", Boolean, user_mapper),
    ],
)
