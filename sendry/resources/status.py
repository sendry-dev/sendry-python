"""
Status resource — system operational status, incident history, latency.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Union

from .._client import AsyncHttpClient, HttpClient
from .._types import (
    GetLatencyParams,
    LatencyStats,
    PaginatedResponse,
    PaginationParams,
    SystemStatus,
)


class Status:
    """
    Synchronous status resource.

    Access via ``sendry.status``.
    """

    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def get_current(self) -> SystemStatus:
        """Get the current operational status of all Sendry components."""
        return self._client.get("/v1/status")

    def get_history(
        self, params: Optional[Union[PaginationParams, Dict[str, Any]]] = None
    ) -> PaginatedResponse:
        """Get a paginated list of resolved incidents."""
        return self._client.get(
            "/v1/status/history", dict(params) if params else None
        )

    def get_latency(
        self, params: Optional[Union[GetLatencyParams, Dict[str, Any]]] = None
    ) -> LatencyStats:
        """Get hourly P50/P95/P99 latency rollups for a component."""
        return self._client.get(
            "/v1/status/latency", dict(params) if params else None
        )


class AsyncStatus:
    """
    Asynchronous status resource.

    Access via ``async_sendr.status``.
    """

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def get_current(self) -> SystemStatus:
        """Get current status. See :meth:`Status.get_current`."""
        return await self._client.get("/v1/status")

    async def get_history(
        self, params: Optional[Union[PaginationParams, Dict[str, Any]]] = None
    ) -> PaginatedResponse:
        """Get incident history. See :meth:`Status.get_history`."""
        return await self._client.get(
            "/v1/status/history", dict(params) if params else None
        )

    async def get_latency(
        self, params: Optional[Union[GetLatencyParams, Dict[str, Any]]] = None
    ) -> LatencyStats:
        """Get latency stats. See :meth:`Status.get_latency`."""
        return await self._client.get(
            "/v1/status/latency", dict(params) if params else None
        )


__all__ = ["Status", "AsyncStatus"]
