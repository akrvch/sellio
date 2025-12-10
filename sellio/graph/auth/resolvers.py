from hiku.engine import pass_context

from sellio.graph import TGraphContext
from sellio.graph.auth.responses import CompleteProfileResponse
from sellio.graph.auth.responses import LogoutResponse
from sellio.graph.auth.responses import RequestAuthCodeResponse
from sellio.graph.auth.responses import VerifyAuthCodeResponse
from sellio.services.auth import complete_user_profile
from sellio.services.auth import create_auth_session
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


@pass_context
async def mutation_logout(
    ctx: TGraphContext, opts: dict[str, str]
) -> LogoutResponse:
    """Logout mutation."""
    await logout()

    return LogoutResponse(
        status="SUCCESS",
        message="Successfully logged out",
    )
