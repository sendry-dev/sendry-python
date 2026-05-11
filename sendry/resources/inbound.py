"""
Inbound resource — list, get, configure inbound email handling.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Union
from urllib.parse import quote

from .._client import AsyncHttpClient, HttpClient
from .._types import (
    InboundConfig,
    InboundEmail,
    PaginatedResponse,
    PaginationParams,
    UpdateInboundConfigParams,
)


class Inbound:
    """
    Synchronous inbound emails resource.

    Access via ``sendry.inbound``.
    """

    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def list(
        self, params: Optional[Union[PaginationParams, Dict[str, Any]]] = None
    ) -> PaginatedResponse:
        """List received inbound emails with cursor pagination."""
        return self._client.get("/v1/inbound", dict(params) if params else None)

    def get(self, inbound_id: str) -> InboundEmail:
        """Get a specific inbound email by ID."""
        return self._client.get(f"/v1/inbound/{quote(inbound_id, safe='')}")

    def get_config(self) -> InboundConfig:
        """Get the inbound webhook forwarding configuration."""
        return self._client.get("/v1/inbound/config")

    def update_config(
        self, params: Union[UpdateInboundConfigParams, Dict[str, Any]]
    ) -> InboundConfig:
        """Update the inbound webhook forwarding configuration."""
        return self._client.put("/v1/inbound/config", dict(params))


class AsyncInbound:
    """
    Asynchronous inbound emails resource.

    Access via ``async_sendr.inbound``.
    """

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def list(
        self, params: Optional[Union[PaginationParams, Dict[str, Any]]] = None
    ) -> PaginatedResponse:
        """List inbound emails. See :meth:`Inbound.list`."""
        return await self._client.get("/v1/inbound", dict(params) if params else None)

    async def get(self, inbound_id: str) -> InboundEmail:
        """Get inbound email. See :meth:`Inbound.get`."""
        return await self._client.get(f"/v1/inbound/{quote(inbound_id, safe='')}")

    async def get_config(self) -> InboundConfig:
        """Get inbound config. See :meth:`Inbound.get_config`."""
        return await self._client.get("/v1/inbound/config")

    async def update_config(
        self, params: Union[UpdateInboundConfigParams, Dict[str, Any]]
    ) -> InboundConfig:
        """Update inbound config. See :meth:`Inbound.update_config`."""
        return await self._client.put("/v1/inbound/config", dict(params))


__all__ = ["Inbound", "AsyncInbound"]
