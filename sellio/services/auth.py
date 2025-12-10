import secrets

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sellio.models.auth_session import AuthSession
from sellio.models.user import User


def generate_otp_from_phone(phone: str) -> str:
    """Generate OTP code from last 4 digits of phone number."""
    # Remove all non-digit characters
    digits = "".join(filter(str.isdigit, phone))
    # Get last 4 digits
    return digits[-4:] if len(digits) >= 4 else digits.zfill(4)


def generate_session_token() -> str:
    """Generate secure random session token."""
    return secrets.token_urlsafe(48)


async def create_auth_session(session: AsyncSession, phone: str) -> AuthSession:
    """Create new auth session with OTP code."""
    otp_code = generate_otp_from_phone(phone)

    auth_session = AuthSession(
        phone=phone,
        otp_code=otp_code,
        expires_at=AuthSession.create_expiration(minutes=5),
        verified=False,
    )

    session.add(auth_session)
    await session.commit()
    await session.refresh(auth_session)

    return auth_session


async def verify_otp_code(
    session: AsyncSession, phone: str, code: str
) -> tuple[AuthSession | None, User | None, bool]:
    """
    Verify OTP code and return auth session, user (if exists), and profile_required flag.

    Returns:
        tuple[AuthSession | None, User | None, bool]:
            - AuthSession if code is valid, None otherwise
            - User if exists, None if needs to be created
            - bool indicating if profile completion is required
    """
    # Find the latest auth session for this phone
    result = await session.execute(
        select(AuthSession)
        .where(
            AuthSession.phone == phone,
            AuthSession.verified == False,  # noqa: E712
        )
        .order_by(AuthSession.created_at.desc())
        .limit(1)
    )
    auth_session = result.scalar_one_or_none()

    if not auth_session or not auth_session.is_valid_code(code):
        return None, None, False

    # Mark session as verified
    auth_session.verified = True
    auth_session.session_token = generate_session_token()

    # Check if user exists
    user_result = await session.execute(select(User).where(User.phone == phone))
    user = user_result.scalar_one_or_none()

    profile_required = False

    if not user:
        # Create new user
        user = User(
            phone=phone,
        )
        session.add(user)
        await session.flush()
        profile_required = True
    else:
        profile_required = not user.is_profile_completed

    # Link session to user
    auth_session.user_id = user.id
    auth_session.expires_at = AuthSession.create_expiration(
        minutes=60 * 24 * 30
    )  # 30 days

    await session.commit()
    await session.refresh(auth_session)
    await session.refresh(user)

    return auth_session, user, profile_required


async def get_user_by_session_token(
    session: AsyncSession, token: str
) -> User | None:
    """Get user by session token."""
    result = await session.execute(
        select(AuthSession).where(
            AuthSession.session_token == token,
            AuthSession.verified == True,  # noqa: E712
        )
    )
    auth_session = result.scalar_one_or_none()

    if not auth_session or auth_session.is_expired():
        return None

    if auth_session.user_id is None:
        return None

    user_result = await session.execute(
        select(User).where(User.id == auth_session.user_id)
    )
    return user_result.scalar_one_or_none()


async def complete_user_profile(
    session: AsyncSession,
    user_id: int,
    first_name: str,
    second_name: str,
    last_name: str,
    email: str | None = None,
) -> User | None:
    """Complete user profile information."""
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        return None

    user.first_name = first_name
    user.second_name = second_name
    user.last_name = last_name
    user.email = email

    await session.commit()
    await session.refresh(user)

    return user
