from hiku.graph import Nothing
from hiku.graph import NothingType

from sellio.graph.user.types import UserResponse
from sellio.services.session import get_current_user


async def link_current_user() -> UserResponse | NothingType:
    """Get current authenticated user."""
    user = await get_current_user()

    if not user:
        return Nothing

    return UserResponse(
        id=user.id,
        phone=user.phone,
        first_name=user.first_name,
        second_name=user.second_name,
        last_name=user.last_name,
        email=user.email,
        is_profile_completed=user.is_profile_completed,
        is_superuser=user.is_superuser,
    )
