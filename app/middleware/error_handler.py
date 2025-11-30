"""Global error handling middleware."""

from typing import Callable

import structlog
from fastapi import Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.exceptions import BaseAPIException
from app.core.templates import is_htmx_request

logger = structlog.get_logger(__name__)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware to handle exceptions globally."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request and handle exceptions.

        Args:
            request: Incoming request
            call_next: Next middleware or route handler

        Returns:
            Response: HTTP response
        """
        try:
            response = await call_next(request)
            return response
        except BaseAPIException as exc:
            logger.warning(
                "api_exception",
                message=exc.message,
                status_code=exc.status_code,
                details=exc.details,
            )

            # Return HTML for HTMX requests, JSON for API requests
            if is_htmx_request(request):
                error_html = f"""
                <div class="p-4 bg-red-100 border border-red-400 rounded">
                    <p class="text-red-800 font-semibold">Error: {exc.message}</p>
                </div>
                """
                return HTMLResponse(
                    status_code=exc.status_code,
                    content=error_html,
                )

            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "error": {
                        "message": exc.message,
                        "details": exc.details,
                    }
                },
            )
        except Exception as exc:
            logger.exception(
                "unhandled_exception",
                exception_type=type(exc).__name__,
                exception_message=str(exc),
            )

            # Return HTML for HTMX requests, JSON for API requests
            if is_htmx_request(request):
                error_html = """
                <div class="p-4 bg-red-100 border border-red-400 rounded">
                    <p class="text-red-800 font-semibold">Internal server error</p>
                </div>
                """
                return HTMLResponse(
                    status_code=500,
                    content=error_html,
                )

            return JSONResponse(
                status_code=500,
                content={
                    "error": {
                        "message": "Internal server error",
                        "details": {},
                    }
                },
            )
