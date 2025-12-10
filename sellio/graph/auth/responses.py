"""Response dataclasses for auth mutations."""

from dataclasses import dataclass


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
