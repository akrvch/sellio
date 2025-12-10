"""Utilities for working with authenticated users in GraphQL context."""

from sellio.models.user import User
from sellio.services.session import get_current_user as _get_current_user


async def require_auth() -> User:
    """
    Get current authenticated user or raise exception.

    Raises:
        ValueError: If user is not authenticated.
    """
    user = await _get_current_user()
    if not user:
        raise ValueError("Authentication required")
    return user
