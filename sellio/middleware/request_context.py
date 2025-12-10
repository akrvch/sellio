"""Middleware for setting request in context and applying pending cookies."""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from sellio.deps.request import get_pending_cookies
from sellio.deps.request import set_request


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Middleware that sets request in contextvars and applies pending cookies to response."""

    async def dispatch(self, request: Request, call_next):
        # Set request in context and initialize pending cookies list
        set_request(request)

        # Call next middleware/endpoint
        response = await call_next(request)

        # Apply all pending cookies to response
        for cookie_params in get_pending_cookies():
            response.set_cookie(**cookie_params)

        return response
