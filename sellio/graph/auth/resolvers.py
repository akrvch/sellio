from hiku.engine import pass_context

from sellio.graph import TGraphContext
from sellio.graph.auth.types import CompleteProfileResponse
from sellio.graph.auth.types import LogoutResponse
from sellio.graph.auth.types import RequestAuthCodeResponse
from sellio.graph.auth.types import UpdateProfileErrorCode
from sellio.graph.auth.types import UpdateProfileResponse
from sellio.graph.auth.types import VerifyAuthCodeResponse
from sellio.services.auth import complete_user_profile
from sellio.services.auth import create_auth_session
from sellio.services.auth import update_user_profile
from sellio.services.auth import verify_otp_code
from sellio.services.session import get_current_user
from sellio.services.session import login
from sellio.services.session import logout


@pass_context
async def mutation_request_auth_code(
    ctx: TGraphContext, opts: dict[str, str]
) -> RequestAuthCodeResponse:
    """Request OTP code mutation."""
    phone = opts["phone"]

    async with ctx["db.session_async"].session() as session:
        await create_auth_session(session, phone)

    return RequestAuthCodeResponse(
        status="CODE_SENT",
        message=f"Verification code sent to {phone}",
    )


@pass_context
async def mutation_verify_auth_code(
    ctx: TGraphContext, opts: dict[str, str]
) -> VerifyAuthCodeResponse:
    """Verify OTP code mutation."""
    phone = opts["phone"]
    code = opts["code"]

    async with ctx["db.session_async"].session() as session:
        auth_session, user, profile_required = await verify_otp_code(
            session, phone, code
        )

        if not auth_session or not user:
            return VerifyAuthCodeResponse(
                status="INVALID_CODE",
                message="Invalid or expired verification code",
                session_token=None,
                user_id=None,
                profile_required=False,
            )

    # Login user (sets cookie)
    await login(user)

    status = "PROFILE_INFO_REQUIRED" if profile_required else "SUCCESS"
    message = (
        "Please complete your profile"
        if profile_required
        else "Successfully authenticated"
    )

    return VerifyAuthCodeResponse(
        status=status,
        message=message,
        session_token=auth_session.session_token,
        user_id=user.id,
        profile_required=profile_required,
    )


@pass_context
async def mutation_complete_profile(
    ctx: TGraphContext, opts: dict[str, str]
) -> CompleteProfileResponse:
    """Complete user profile mutation."""
    # Get current user from cookie
    user = await get_current_user()

    if not user:
        return CompleteProfileResponse(
            status="ERROR",
            message="Authentication required",
            user_id=None,
        )

    first_name = opts["firstName"]
    second_name = opts["secondName"]
    last_name = opts["lastName"]
    email = opts.get("email")

    async with ctx["db.session_async"].session() as session:
        # Complete profile
        updated_user = await complete_user_profile(
            session,
            user.id,
            first_name,
            second_name,
            last_name,
            email,
        )

        if not updated_user:
            return CompleteProfileResponse(
                status="ERROR",
                message="Failed to update profile",
                user_id=None,
            )

        return CompleteProfileResponse(
            status="SUCCESS",
            message="Profile completed successfully",
            user_id=updated_user.id,
        )


async def mutation_logout() -> LogoutResponse:
    """Logout mutation."""
    await logout()

    return LogoutResponse(
        status="SUCCESS",
        message="Successfully logged out",
    )


@pass_context
async def mutation_update_profile(
    ctx: TGraphContext, opts: dict[str, str]
) -> UpdateProfileResponse:
    """Update user profile mutation."""
    # Get current user from cookie
    user = await get_current_user()

    if not user:
        return UpdateProfileResponse(
            status="ERROR",
            message="Необхідна авторизація",
            user_id=None,
            error_code=UpdateProfileErrorCode.AUTH_REQUIRED,
            missing_fields=None,
        )

    first_name = opts.get("firstName")
    second_name = opts.get("secondName")
    last_name = opts.get("lastName")
    email = opts.get("email")

    # Validate that first_name and last_name cannot be empty strings
    missing_fields = []
    if first_name is not None and not first_name.strip():
        missing_fields.append("firstName")
    if last_name is not None and not last_name.strip():
        missing_fields.append("lastName")

    if missing_fields:
        return UpdateProfileResponse(
            status="ERROR",
            message="Обов'язкові поля не можуть бути пустими",
            user_id=None,
            error_code=UpdateProfileErrorCode.MISSING_REQUIRED_FIELDS,
            missing_fields=tuple(missing_fields),
        )

    async with ctx["db.session_async"].session() as session:
        # Update profile
        updated_user = await update_user_profile(
            session,
            user.id,
            first_name=first_name,
            second_name=second_name,
            last_name=last_name,
            email=email,
        )

        if not updated_user:
            return UpdateProfileResponse(
                status="ERROR",
                message="Не вдалося оновити профіль",
                user_id=None,
                error_code=UpdateProfileErrorCode.UPDATE_FAILED,
                missing_fields=None,
            )

        return UpdateProfileResponse(
            status="SUCCESS",
            message="Профіль успішно оновлено",
            user_id=updated_user.id,
            error_code=None,
            missing_fields=None,
        )
