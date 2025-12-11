from dataclasses import dataclass
from enum import Enum


class AuthStatus(str, Enum):
    CODE_SENT = "CODE_SENT"
    SUCCESS = "SUCCESS"
    PROFILE_INFO_REQUIRED = "PROFILE_INFO_REQUIRED"
    INVALID_CODE = "INVALID_CODE"
    EXPIRED_CODE = "EXPIRED_CODE"


class UpdateProfileErrorCode(str, Enum):
    AUTH_REQUIRED = "AUTH_REQUIRED"
    MISSING_REQUIRED_FIELDS = "MISSING_REQUIRED_FIELDS"
    UPDATE_FAILED = "UPDATE_FAILED"


@dataclass(frozen=True)
class RequestAuthCodeResponse:
    status: str
    message: str


@dataclass(frozen=True)
class VerifyAuthCodeResponse:
    status: str
    message: str
    session_token: str | None
    user_id: int | None
    profile_required: bool


@dataclass(frozen=True)
class CompleteProfileResponse:
    status: str
    message: str
    user_id: int | None


@dataclass(frozen=True)
class LogoutResponse:
    status: str
    message: str


@dataclass(frozen=True)
class UpdateProfileResponse:
    status: str
    message: str
    user_id: int | None
    error_code: str | None
    missing_fields: tuple[str, ...] | None
