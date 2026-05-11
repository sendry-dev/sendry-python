"""
Test emails resource — list and get test-mode captured emails.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Union
from urllib.parse import quote

from .._client import AsyncHttpClient, HttpClient
from .._types import (
    PaginatedResponse,
    PaginationParams,
    TestEmail,
)


class TestEmails:
    """
    Synchronous test emails resource.

    Access via ``sendry.test_emails``.
    """

    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def list(
        self, params: Optional[Union[PaginationParams, Dict[str, Any]]] = None
    ) -> PaginatedResponse:
        """List test emails captured in test mode with cursor pagination."""
        return self._client.get(
            "/v1/test-emails", dict(params) if params else None
        )

    def get(self, test_email_id: str) -> TestEmail:
        """Get a specific test email by ID including HTML and plain text body."""
        return self._client.get(
            f"/v1/test-emails/{quote(test_email_id, safe='')}"
        )


class AsyncTestEmails:
    """
    Asynchronous test emails resource.

    Access via ``async_sendr.test_emails``.
    """

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def list(
        self, params: Optional[Union[PaginationParams, Dict[str, Any]]] = None
    ) -> PaginatedResponse:
        """List test emails. See :meth:`TestEmails.list`."""
        return await self._client.get(
            "/v1/test-emails", dict(params) if params else None
        )

    async def get(self, test_email_id: str) -> TestEmail:
        """Get test email. See :meth:`TestEmails.get`."""
        return await self._client.get(
            f"/v1/test-emails/{quote(test_email_id, safe='')}"
        )


__all__ = ["TestEmails", "AsyncTestEmails"]
