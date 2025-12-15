"""Response dataclasses for user queries."""

from dataclasses import dataclass


@dataclass(frozen=True)
class UserResponse:
    id: int
    phone: str
    first_name: str | None
    second_name: str | None
    last_name: str | None
    email: str | None
    is_profile_completed: bool
    is_superuser: bool
