from hiku.graph import Field
from hiku.graph import Node
from hiku.types import Boolean
from hiku.types import Integer
from hiku.types import Optional
from hiku.types import String

from sellio.graph import UniversalMapper

request_auth_code_mapper = UniversalMapper("RequestAuthCodeResponse")
verify_auth_code_mapper = UniversalMapper("VerifyAuthCodeResponse")
complete_profile_mapper = UniversalMapper("CompleteProfileResponse")
logout_mapper = UniversalMapper("LogoutResponse")

# Response for requestAuthCode mutation
RequestAuthCodeNode = Node(
    "RequestAuthCodeResponse",
    [
        Field("status", String, request_auth_code_mapper),
        Field("message", String, request_auth_code_mapper),
    ],
)

# Response for verifyAuthCode mutation
VerifyAuthCodeNode = Node(
    "VerifyAuthCodeResponse",
    [
        Field("status", String, verify_auth_code_mapper),
        Field("message", String, verify_auth_code_mapper),
        Field("userId", Optional[Integer], verify_auth_code_mapper),
        Field("profileRequired", Boolean, verify_auth_code_mapper),
    ],
)

# Response for completeProfile mutation
CompleteProfileNode = Node(
    "CompleteProfileResponse",
    [
        Field("status", String, complete_profile_mapper),
        Field("message", String, complete_profile_mapper),
        Field("userId", Optional[Integer], complete_profile_mapper),
    ],
)

# Response for logout mutation
LogoutNode = Node(
    "LogoutResponse",
    [
        Field("status", String, logout_mapper),
        Field("message", String, logout_mapper),
    ],
)
