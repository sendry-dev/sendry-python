"""
Events resource — ingest, list, and get event records that drive automations.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Union
from urllib.parse import quote

from .._client import AsyncHttpClient, HttpClient
from .._types import (
    IngestedEvent,
    IngestEventParams,
    ListEventsParams,
    PaginatedResponse,
)


class Events:
    """
    Synchronous events resource.

    Access via ``sendry.events``.
    """

    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def ingest(
        self, params: Union[IngestEventParams, Dict[str, Any]]
    ) -> IngestedEvent:
        """Ingest an event that may trigger automation runs."""
        return self._client.post("/v1/events", dict(params))

    def list(
        self, params: Optional[Union[ListEventsParams, Dict[str, Any]]] = None
    ) -> PaginatedResponse:
        """List ingested events with cursor pagination."""
        return self._client.get("/v1/events", dict(params) if params else None)

    def get(self, event_id: str) -> IngestedEvent:
        """Get a single ingested event by ID."""
        return self._client.get(f"/v1/events/{quote(event_id, safe='')}")


class AsyncEvents:
    """
    Asynchronous events resource.

    Access via ``async_sendr.events``.
    """

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def ingest(
        self, params: Union[IngestEventParams, Dict[str, Any]]
    ) -> IngestedEvent:
        """Ingest event. See :meth:`Events.ingest`."""
        return await self._client.post("/v1/events", dict(params))

    async def list(
        self, params: Optional[Union[ListEventsParams, Dict[str, Any]]] = None
    ) -> PaginatedResponse:
        """List events. See :meth:`Events.list`."""
        return await self._client.get("/v1/events", dict(params) if params else None)

    async def get(self, event_id: str) -> IngestedEvent:
        """Get event. See :meth:`Events.get`."""
        return await self._client.get(f"/v1/events/{quote(event_id, safe='')}")


__all__ = ["Events", "AsyncEvents"]
