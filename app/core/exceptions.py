"""Custom exception classes for the application."""

from typing import Any, Optional


class BaseAPIException(Exception):
    """Base exception class for API errors."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        """
        Initialize the exception.

        Args:
            message: Error message
            status_code: HTTP status code
            details: Additional error details
        """
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class NotFoundError(BaseAPIException):
    """Exception raised when a resource is not found."""

    def __init__(
        self,
        message: str = "Resource not found",
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message=message, status_code=404, details=details)


class ValidationError(BaseAPIException):
    """Exception raised for validation errors."""

    def __init__(
        self,
        message: str = "Validation error",
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message=message, status_code=422, details=details)


class UnauthorizedError(BaseAPIException):
    """Exception raised for unauthorized access."""

    def __init__(
        self, message: str = "Unauthorized", details: Optional[dict[str, Any]] = None
    ) -> None:
        super().__init__(message=message, status_code=401, details=details)


class ForbiddenError(BaseAPIException):
    """Exception raised for forbidden access."""

    def __init__(
        self, message: str = "Forbidden", details: Optional[dict[str, Any]] = None
    ) -> None:
        super().__init__(message=message, status_code=403, details=details)
