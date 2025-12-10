"""Global access to current request and deferred cookie setting via contextvars."""

from contextvars import ContextVar
from typing import Any

from starlette.requests import Request

# Context variables
_request_ctx_var: ContextVar[Request | None] = ContextVar(
    "request", default=None
)
_pending_cookies_ctx_var: ContextVar[list[dict[str, Any]]] = ContextVar(
    "pending_cookies", default=None
)


def set_request(request: Request) -> None:
    """Set current request in context."""
    _request_ctx_var.set(request)
    # Initialize empty list for pending cookies
    _pending_cookies_ctx_var.set([])


def get_request() -> Request | None:
    """Get current request from context."""
    return _request_ctx_var.get()


def set_cookie(
    key: str,
    value: str = "",
    max_age: int | None = None,
    expires: int | None = None,
    path: str = "/",
    domain: str | None = None,
    secure: bool = False,
    httponly: bool = False,
    samesite: str = "lax",
) -> None:
    """
    Queue cookie to be set in response.

    The cookie will be applied to response by middleware.

    Raises:
        RuntimeError: If called outside request context.
    """
    pending_cookies = _pending_cookies_ctx_var.get()
    if pending_cookies is None:
        raise RuntimeError("No request context available")

    pending_cookies.append(
        {
            "key": key,
            "value": value,
            "max_age": max_age,
            "expires": expires,
            "path": path,
            "domain": domain,
            "secure": secure,
            "httponly": httponly,
            "samesite": samesite,
        }
    )


def get_pending_cookies() -> list[dict[str, Any]]:
    """Get list of cookies queued to be set."""
    return _pending_cookies_ctx_var.get() or []


def get_cookie(key: str, default: Any = None) -> Any:
    """
    Get cookie from current request.

    Raises:
        RuntimeError: If called outside request context.
    """
    request = get_request()
    if request is None:
        raise RuntimeError("No request available in current context")

    return request.cookies.get(key, default)
