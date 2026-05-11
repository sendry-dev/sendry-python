"""
Unsubscribes resource — list, create, create_batch, get, remove.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Union
from urllib.parse import quote

from .._client import AsyncHttpClient, HttpClient
from .._types import (
    BatchUnsubscribeParams,
    BatchUnsubscribeResponse,
    CreateUnsubscribeParams,
    DeleteResponse,
    ListUnsubscribesParams,
    PaginatedResponse,
    UnsubscribeEntry,
)


class Unsubscribes:
    """
    Synchronous unsubscribes resource.

    Access via ``sendry.unsubscribes``.
    """

    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def list(
        self, params: Optional[Union[ListUnsubscribesParams, Dict[str, Any]]] = None
    ) -> PaginatedResponse:
        """
        List unsubscribed email addresses.

        Args:
            params: Optional filters — ``email``, ``list_id``, ``cursor``, ``limit``.

        Returns:
            PaginatedResponse of UnsubscribeEntry objects.
        """
        return self._client.get("/v1/unsubscribes", dict(params) if params else None)

    def create(
        self, params: Union[CreateUnsubscribeParams, Dict[str, Any]]
    ) -> UnsubscribeEntry:
        """
        Add a single email address to the unsubscribe list.

        Args:
            params: Must include ``email``. Optional ``list_id`` and ``reason``.

        Returns:
            The created UnsubscribeEntry.

        Example::

            entry = sendry.unsubscribes.create({
                "email": "user@example.com",
                "list_id": "newsletter",
                "reason": "User clicked unsubscribe link",
            })
        """
        return self._client.post("/v1/unsubscribes", dict(params))

    def create_batch(
        self, params: Union[BatchUnsubscribeParams, Dict[str, Any]]
    ) -> BatchUnsubscribeResponse:
        """
        Batch-add up to 1000 email addresses to the unsubscribe list.

        Args:
            params: Must include ``emails`` list. Optional ``list_id`` and ``reason``.

        Returns:
            BatchUnsubscribeResponse with ``inserted`` count.

        Example::

            result = sendry.unsubscribes.create_batch({
                "emails": ["a@example.com", "b@example.com"],
                "list_id": "newsletter",
            })
            print(f"Inserted {result['inserted']} unsubscribes")
        """
        return self._client.post("/v1/unsubscribes/batch", dict(params))

    def get(self, unsubscribe_id: str) -> UnsubscribeEntry:
        """
        Get a single unsubscribe record by ID.

        Args:
            unsubscribe_id: The unsubscribe record ID (e.g. ``us_abc123``).

        Returns:
            UnsubscribeEntry with email, list_id, and reason.
        """
        return self._client.get(f"/v1/unsubscribes/{quote(unsubscribe_id, safe='')}")

    def remove(self, unsubscribe_id: str) -> DeleteResponse:
        """
        Remove an unsubscribe record by ID (re-subscribes the address).

        Args:
            unsubscribe_id: The unsubscribe record ID.

        Returns:
            DeleteResponse acknowledging the removal.
        """
        return self._client.delete(f"/v1/unsubscribes/{quote(unsubscribe_id, safe='')}")


class AsyncUnsubscribes:
    """
    Asynchronous unsubscribes resource.

    Access via ``async_sendr.unsubscribes``.
    """

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def list(
        self, params: Optional[Union[ListUnsubscribesParams, Dict[str, Any]]] = None
    ) -> PaginatedResponse:
        """List unsubscribes. See :meth:`Unsubscribes.list`."""
        return await self._client.get("/v1/unsubscribes", dict(params) if params else None)

    async def create(
        self, params: Union[CreateUnsubscribeParams, Dict[str, Any]]
    ) -> UnsubscribeEntry:
        """Add an unsubscribe. See :meth:`Unsubscribes.create`."""
        return await self._client.post("/v1/unsubscribes", dict(params))

    async def create_batch(
        self, params: Union[BatchUnsubscribeParams, Dict[str, Any]]
    ) -> BatchUnsubscribeResponse:
        """Batch-add unsubscribes. See :meth:`Unsubscribes.create_batch`."""
        return await self._client.post("/v1/unsubscribes/batch", dict(params))

    async def get(self, unsubscribe_id: str) -> UnsubscribeEntry:
        """Get an unsubscribe record. See :meth:`Unsubscribes.get`."""
        return await self._client.get(f"/v1/unsubscribes/{quote(unsubscribe_id, safe='')}")

    async def remove(self, unsubscribe_id: str) -> DeleteResponse:
        """Remove an unsubscribe record. See :meth:`Unsubscribes.remove`."""
        return await self._client.delete(f"/v1/unsubscribes/{quote(unsubscribe_id, safe='')}")


__all__ = ["Unsubscribes", "AsyncUnsubscribes"]
