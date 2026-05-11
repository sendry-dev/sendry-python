"""
Exception classes for the Sendry Python SDK.
"""

from __future__ import annotations

from typing import Any, Optional


class SendryError(Exception):
    """Base class for all Sendry SDK errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.message!r})"


class ApiError(SendryError):
    """
    The API returned an error response (4xx or 5xx).

    Attributes:
        status_code: HTTP status code returned by the API.
        code: Machine-readable error code string from the API.
        message: Human-readable error message.
        details: Optional additional error details (validation fields, etc.).
    """

    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        details: Optional[Any] = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.details = details

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"status_code={self.status_code}, "
            f"code={self.code!r}, "
            f"message={self.message!r})"
        )


class AuthenticationError(ApiError):
    """
    401 Unauthorized — invalid or missing API key.

    Raised when the API key is missing, malformed, or revoked.
    """

    def __init__(self, message: str = "Invalid API key") -> None:
        super().__init__(401, "authentication_error", message)


class ValidationError(ApiError):
    """
    422 Unprocessable Entity — request body or parameters failed validation.

    The ``details`` attribute contains field-level validation errors.
    """

    def __init__(self, message: str, details: Optional[Any] = None) -> None:
        super().__init__(422, "validation_error", message, details)


class RateLimitError(ApiError):
    """
    429 Too Many Requests — the rate limit has been exceeded.

    Attributes:
        retry_after: Seconds to wait before retrying, if provided by the API.
    """

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: Optional[int] = None,
    ) -> None:
        super().__init__(429, "rate_limit_error", message)
        self.retry_after = retry_after

    def __repr__(self) -> str:
        return (
            f"RateLimitError("
            f"message={self.message!r}, "
            f"retry_after={self.retry_after})"
        )


class NotFoundError(ApiError):
    """
    404 Not Found — the requested resource does not exist.
    """

    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(404, "not_found", message)


class NetworkError(SendryError):
    """
    A network-level error occurred (connection refused, DNS failure, timeout, etc.).

    Attributes:
        cause: The original exception that triggered this error, if any.
    """

    def __init__(self, message: str, cause: Optional[Exception] = None) -> None:
        super().__init__(message)
        self.cause = cause

    def __repr__(self) -> str:
        return f"NetworkError({self.message!r})"


__all__ = [
    "SendryError",
    "ApiError",
    "AuthenticationError",
    "ValidationError",
    "RateLimitError",
    "NotFoundError",
    "NetworkError",
]
