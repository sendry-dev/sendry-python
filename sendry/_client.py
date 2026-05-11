"""
HTTP client for the Sendry Python SDK.

Provides both synchronous (using httpx) and asynchronous variants with:
- Automatic retries with exponential backoff on 5xx and network errors
- Retry-After header respect on 429 responses
- Typed exception mapping based on HTTP status codes
- Configurable timeout and User-Agent
"""

from __future__ import annotations

import time
from typing import Any, Dict, Optional, Type, Union
from urllib.parse import urlencode

import httpx

from ._exceptions import (
    ApiError,
    AuthenticationError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    SendryError,
    ValidationError,
)

DEFAULT_BASE_URL = "https://api.sendry.online"
DEFAULT_TIMEOUT = 30.0
DEFAULT_RETRIES = 3
USER_AGENT = "sendry-python/0.2.0"

# Backoff delays in seconds: 1s, 2s, 4s
_BACKOFF_DELAYS = [1, 2, 4]


def _build_url(base_url: str, path: str, params: Optional[Dict[str, Any]] = None) -> str:
    """Construct a full URL with optional query string parameters."""
    url = base_url.rstrip("/") + path
    if params:
        filtered = {k: v for k, v in params.items() if v is not None}
        if filtered:
            url = f"{url}?{urlencode(filtered)}"
    return url


def _parse_error_body(
    response: httpx.Response,
) -> tuple[str, str, Any]:
    """
    Parse the error body from an API response.

    Returns:
        Tuple of (code, message, details).
    """
    try:
        body = response.json()
        err = body.get("error", {}) if isinstance(body, dict) else {}
        code = err.get("code", "unknown_error") if isinstance(err, dict) else "unknown_error"
        message = err.get("message", response.reason_phrase) if isinstance(err, dict) else response.reason_phrase
        details = err.get("details") if isinstance(err, dict) else None
        return code, message, details
    except Exception:
        return "unknown_error", response.reason_phrase or "Unknown error", None


def _raise_for_status(response: httpx.Response) -> None:
    """Map an HTTP error response to the appropriate SDK exception."""
    if response.is_success:
        return

    code, message, details = _parse_error_body(response)
    status = response.status_code

    if status == 401:
        raise AuthenticationError(message)
    if status == 404:
        raise NotFoundError(message)
    if status == 422:
        raise ValidationError(message, details)
    if status == 429:
        retry_after_header = response.headers.get("Retry-After")
        retry_after = int(retry_after_header) if retry_after_header else None
        raise RateLimitError(message, retry_after=retry_after)

    raise ApiError(status, code, message, details)


def _should_retry(exc: Exception, attempt: int, max_retries: int) -> bool:
    """Return True if the request should be retried."""
    if attempt >= max_retries:
        return False
    if isinstance(exc, (NetworkError,)):
        return True
    if isinstance(exc, ApiError) and exc.status_code >= 500:
        return True
    return False


class HttpClient:
    """
    Synchronous HTTP client backed by httpx.

    Not intended for direct use — access it through :class:`Sendry`.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        retries: int = DEFAULT_RETRIES,
        default_headers: Optional[Dict[str, str]] = None,
    ) -> None:
        if not api_key:
            raise ValueError(
                "Missing API key. Pass it to the Sendry constructor: Sendry('sn_live_...')"
            )
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._retries = retries
        self._default_headers: Dict[str, str] = default_headers or {}

    def _headers(self, extra: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "User-Agent": USER_AGENT,
            **self._default_headers,
        }
        if extra:
            headers.update(extra)
        return headers

    def request(
        self,
        method: str,
        path: str,
        *,
        body: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> Any:
        """
        Execute an HTTP request with automatic retry logic.

        Args:
            method: HTTP verb (GET, POST, PUT, PATCH, DELETE).
            path: API path (e.g. ``/v1/emails``).
            body: Request body to JSON-serialize (for POST/PUT/PATCH).
            params: Query string parameters.
            timeout: Per-request timeout override in seconds.

        Returns:
            Parsed JSON response body, or ``None`` for 204 No Content.

        Raises:
            AuthenticationError: On 401.
            NotFoundError: On 404.
            ValidationError: On 422.
            RateLimitError: On 429.
            ApiError: On other 4xx/5xx responses.
            NetworkError: On connection or timeout failures.
        """
        url = _build_url(self._base_url, path, params)
        effective_timeout = timeout if timeout is not None else self._timeout

        headers = self._headers()
        if body is not None:
            headers["Content-Type"] = "application/json"

        last_error: Optional[Exception] = None

        for attempt in range(self._retries + 1):
            if attempt > 0:
                delay_idx = min(attempt - 1, len(_BACKOFF_DELAYS) - 1)
                time.sleep(_BACKOFF_DELAYS[delay_idx])

            try:
                with httpx.Client(timeout=effective_timeout) as client:
                    response = client.request(
                        method,
                        url,
                        headers=headers,
                        json=body,
                    )

                if response.status_code == 204:
                    return None

                if response.is_success:
                    return response.json()

                # Check if we should even try to retry
                code, message, details = _parse_error_body(response)
                status = response.status_code

                # Non-retryable client errors
                if status in (401, 404, 422):
                    _raise_for_status(response)

                if status == 429:
                    _raise_for_status(response)

                # Other 4xx — don't retry
                if 400 <= status < 500:
                    raise ApiError(status, code, message, details)

                # 5xx — retry
                last_error = ApiError(status, code, message, details)

            except (AuthenticationError, NotFoundError, ValidationError, RateLimitError, ApiError) as exc:
                # Re-raise non-retryable errors immediately
                if not isinstance(exc, ApiError) or exc.status_code < 500:
                    raise
                last_error = exc
            except httpx.TimeoutException as exc:
                last_error = NetworkError(f"Request timed out after {effective_timeout}s", exc)
            except httpx.NetworkError as exc:
                last_error = NetworkError(str(exc), exc)
            except Exception as exc:
                raise NetworkError(f"Unexpected error: {exc}", exc) from exc

            if not _should_retry(last_error, attempt, self._retries):
                break

        assert last_error is not None
        raise last_error

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Send a GET request."""
        return self.request("GET", path, params=params)

    def post(self, path: str, body: Optional[Any] = None) -> Any:
        """Send a POST request."""
        return self.request("POST", path, body=body)

    def put(self, path: str, body: Optional[Any] = None) -> Any:
        """Send a PUT request."""
        return self.request("PUT", path, body=body)

    def patch(self, path: str, body: Optional[Any] = None) -> Any:
        """Send a PATCH request."""
        return self.request("PATCH", path, body=body)

    def delete(self, path: str) -> Any:
        """Send a DELETE request."""
        return self.request("DELETE", path)


class AsyncHttpClient:
    """
    Asynchronous HTTP client backed by httpx.AsyncClient.

    Not intended for direct use — access it through :class:`AsyncSendry`.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        retries: int = DEFAULT_RETRIES,
        default_headers: Optional[Dict[str, str]] = None,
    ) -> None:
        if not api_key:
            raise ValueError(
                "Missing API key. Pass it to the AsyncSendry constructor: AsyncSendry('sn_live_...')"
            )
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._retries = retries
        self._default_headers: Dict[str, str] = default_headers or {}

    def _headers(self, extra: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "User-Agent": USER_AGENT,
            **self._default_headers,
        }
        if extra:
            headers.update(extra)
        return headers

    async def request(
        self,
        method: str,
        path: str,
        *,
        body: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> Any:
        """
        Execute an async HTTP request with automatic retry logic.

        Args:
            method: HTTP verb (GET, POST, PUT, PATCH, DELETE).
            path: API path (e.g. ``/v1/emails``).
            body: Request body to JSON-serialize (for POST/PUT/PATCH).
            params: Query string parameters.
            timeout: Per-request timeout override in seconds.

        Returns:
            Parsed JSON response body, or ``None`` for 204 No Content.

        Raises:
            AuthenticationError: On 401.
            NotFoundError: On 404.
            ValidationError: On 422.
            RateLimitError: On 429.
            ApiError: On other 4xx/5xx responses.
            NetworkError: On connection or timeout failures.
        """
        import asyncio

        url = _build_url(self._base_url, path, params)
        effective_timeout = timeout if timeout is not None else self._timeout

        headers = self._headers()
        if body is not None:
            headers["Content-Type"] = "application/json"

        last_error: Optional[Exception] = None

        for attempt in range(self._retries + 1):
            if attempt > 0:
                delay_idx = min(attempt - 1, len(_BACKOFF_DELAYS) - 1)
                await asyncio.sleep(_BACKOFF_DELAYS[delay_idx])

            try:
                async with httpx.AsyncClient(timeout=effective_timeout) as client:
                    response = await client.request(
                        method,
                        url,
                        headers=headers,
                        json=body,
                    )

                if response.status_code == 204:
                    return None

                if response.is_success:
                    return response.json()

                code, message, details = _parse_error_body(response)
                status = response.status_code

                if status in (401, 404, 422, 429):
                    _raise_for_status(response)

                if 400 <= status < 500:
                    raise ApiError(status, code, message, details)

                last_error = ApiError(status, code, message, details)

            except (AuthenticationError, NotFoundError, ValidationError, RateLimitError, ApiError) as exc:
                if not isinstance(exc, ApiError) or exc.status_code < 500:
                    raise
                last_error = exc
            except httpx.TimeoutException as exc:
                last_error = NetworkError(f"Request timed out after {effective_timeout}s", exc)
            except httpx.NetworkError as exc:
                last_error = NetworkError(str(exc), exc)
            except Exception as exc:
                raise NetworkError(f"Unexpected error: {exc}", exc) from exc

            if not _should_retry(last_error, attempt, self._retries):
                break

        assert last_error is not None
        raise last_error

    async def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Send an async GET request."""
        return await self.request("GET", path, params=params)

    async def post(self, path: str, body: Optional[Any] = None) -> Any:
        """Send an async POST request."""
        return await self.request("POST", path, body=body)

    async def put(self, path: str, body: Optional[Any] = None) -> Any:
        """Send an async PUT request."""
        return await self.request("PUT", path, body=body)

    async def patch(self, path: str, body: Optional[Any] = None) -> Any:
        """Send an async PATCH request."""
        return await self.request("PATCH", path, body=body)

    async def delete(self, path: str) -> Any:
        """Send an async DELETE request."""
        return await self.request("DELETE", path)


__all__ = ["HttpClient", "AsyncHttpClient"]
