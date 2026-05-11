"""
Suppression resource — list, add, remove suppressed email addresses.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Union
from urllib.parse import quote

from .._client import AsyncHttpClient, HttpClient
from .._types import (
    AddSuppressionParams,
    DeleteResponse,
    PaginatedResponse,
    PaginationParams,
    SuppressionEntry,
)


class Suppression:
    """
    Synchronous suppression list resource.

    Access via ``sendry.suppression``.
    """

    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def list(self, params: Optional[Union[PaginationParams, Dict[str, Any]]] = None) -> PaginatedResponse:
        """
        List all suppressed email addresses.

        Suppressed addresses include hard bounces, spam complaints, manual
        additions, and unsubscribes.

        Args:
            params: Optional ``limit`` and ``cursor`` for pagination.

        Returns:
            PaginatedResponse of SuppressionEntry objects.
        """
        return self._client.get("/v1/suppression", dict(params) if params else None)

    def add(self, params: Union[AddSuppressionParams, Dict[str, Any]]) -> SuppressionEntry:
        """
        Manually add an email address to the suppression list.

        Args:
            params: Must include ``email``. Optional ``reason``
                (``"hard_bounce"``, ``"complaint"``, ``"unsubscribe"``, ``"manual"``).

        Returns:
            SuppressionEntry for the newly added address.

        Example::

            sendry.suppression.add({
                "email": "bounced@example.com",
                "reason": "hard_bounce",
            })
        """
        return self._client.post("/v1/suppression", dict(params))

    def remove(self, email: str) -> DeleteResponse:
        """
        Remove an email address from the suppression list.

        After removal, the address can receive emails again.

        Args:
            email: The email address to remove.

        Returns:
            DeleteResponse acknowledging the removal.

        Example::

            sendry.suppression.remove("user@example.com")
        """
        return self._client.delete(f"/v1/suppression/{quote(email, safe='')}")


class AsyncSuppression:
    """
    Asynchronous suppression list resource.

    Access via ``async_sendr.suppression``.
    """

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def list(
        self, params: Optional[Union[PaginationParams, Dict[str, Any]]] = None
    ) -> PaginatedResponse:
        """List suppressed addresses. See :meth:`Suppression.list`."""
        return await self._client.get("/v1/suppression", dict(params) if params else None)

    async def add(
        self, params: Union[AddSuppressionParams, Dict[str, Any]]
    ) -> SuppressionEntry:
        """Add a suppression entry. See :meth:`Suppression.add`."""
        return await self._client.post("/v1/suppression", dict(params))

    async def remove(self, email: str) -> DeleteResponse:
        """Remove a suppression entry. See :meth:`Suppression.remove`."""
        return await self._client.delete(f"/v1/suppression/{quote(email, safe='')}")


__all__ = ["Suppression", "AsyncSuppression"]
