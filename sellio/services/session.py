"""User session management with global request/response access."""

import secrets
from datetime import datetime

from sqlalchemy import select

from sellio.deps.request import get_cookie
from sellio.deps.request import set_cookie
from sellio.models.auth_session import AuthSession
from sellio.models.user import User
from sellio.services.db import main_db

AUTH_COOKIE_NAME = "sellio_auth"


def _generate_session_token() -> str:
    """Generate secure random session token."""
    return secrets.token_urlsafe(48)


async def login(user: User) -> None:
    """
    Login user by creating session and setting auth cookie.

    Args:
        user: User instance to login
    """
    async with main_db.session() as session:
        # Create session token
        session_token = _generate_session_token()

        # Create auth session in database
        auth_session = AuthSession(
            phone=user.phone,
            otp_code="",  # Not needed for login
            session_token=session_token,
            user_id=user.id,
            created_at=datetime.utcnow(),
            expires_at=AuthSession.create_expiration(
                minutes=60 * 24 * 30
            ),  # 30 days
            verified=True,
        )

        session.add(auth_session)
        await session.commit()

    # Set auth cookie
    set_cookie(
        key=AUTH_COOKIE_NAME,
        value=session_token,
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax",
        max_age=60 * 60 * 24 * 30,  # 30 days
    )


async def logout() -> None:
    """Logout current user by removing auth cookie and invalidating session."""
    # Get current session token
    session_token = get_cookie(AUTH_COOKIE_NAME)

    if session_token:
        # Invalidate session in database
        async with main_db.session() as session:
            result = await session.execute(
                select(AuthSession).where(
                    AuthSession.session_token == session_token
                )
            )
            auth_session = result.scalar_one_or_none()

            if auth_session:
                # Mark as expired
                auth_session.expires_at = datetime.utcnow()
                await session.commit()

    # Remove cookie (set it to expire immediately)
    set_cookie(
        key=AUTH_COOKIE_NAME,
        value="",
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=0,  # Expire immediately
    )


async def get_current_user() -> User | None:
    """
    Get current authenticated user from cookie.

    Returns:
        User instance if authenticated, None otherwise.
    """
    session_token = get_cookie(AUTH_COOKIE_NAME)
    if not session_token:
        return None

    async with main_db.session() as session:
        # Get auth session
        result = await session.execute(
            select(AuthSession).where(
                AuthSession.session_token == session_token,
                AuthSession.verified == True,  # noqa: E712
            )
        )
        auth_session = result.scalar_one_or_none()

        if not auth_session or auth_session.is_expired():
            return None

        if auth_session.user_id is None:
            return None

        # Get user
        user_result = await session.execute(
            select(User).where(User.id == auth_session.user_id)
        )
        user = user_result.scalar_one_or_none()
        return user
