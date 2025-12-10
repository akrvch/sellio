from hiku.graph import Link
from hiku.graph import Option
from hiku.types import Optional
from hiku.types import String
from hiku.types import TypeRef

from sellio.graph.auth.resolvers import mutation_complete_profile
from sellio.graph.auth.resolvers import mutation_logout
from sellio.graph.auth.resolvers import mutation_request_auth_code
from sellio.graph.auth.resolvers import mutation_verify_auth_code

RequestAuthCodeLink = Link(
    "requestAuthCode",
    TypeRef["RequestAuthCodeResponse"],
    mutation_request_auth_code,
    options=[
        Option("phone", String),
    ],
    requires=None,
)

VerifyAuthCodeLink = Link(
    "verifyAuthCode",
    TypeRef["VerifyAuthCodeResponse"],
    mutation_verify_auth_code,
    options=[
        Option("phone", String),
        Option("code", String),
    ],
    requires=None,
)

CompleteProfileLink = Link(
    "completeProfile",
    TypeRef["CompleteProfileResponse"],
    mutation_complete_profile,
    options=[
        Option("firstName", String),
        Option("secondName", String),
        Option("lastName", String),
        Option("email", Optional[String], default=None),
    ],
    requires=None,
)

LogoutLink = Link(
    "logout",
    TypeRef["LogoutResponse"],
    mutation_logout,
    options=[],
    requires=None,
)
