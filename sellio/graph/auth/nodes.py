from hiku.graph import Field
from hiku.graph import Node
from hiku.types import Boolean, EnumRef
from hiku.types import Integer
from hiku.types import Optional
from hiku.types import Sequence
from hiku.types import String

from sellio.graph import UniversalMapper

request_auth_code_mapper = UniversalMapper("RequestAuthCodeResponse")
verify_auth_code_mapper = UniversalMapper("VerifyAuthCodeResponse")
complete_profile_mapper = UniversalMapper("CompleteProfileResponse")
logout_mapper = UniversalMapper("LogoutResponse")
update_profile_mapper = UniversalMapper("UpdateProfileResponse")

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

# Response for updateProfile mutation
UpdateProfileNode = Node(
    "UpdateProfileResponse",
    [
        Field("status", String, update_profile_mapper),
        Field("message", String, update_profile_mapper),
        Field("userId", Optional[Integer], update_profile_mapper),
        Field("errorCode", Optional[EnumRef["UpdateProfileErrorCode"]], update_profile_mapper),
        Field("missingFields", Optional[Sequence[String]], update_profile_mapper),
    ],
)
