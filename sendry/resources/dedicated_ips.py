"""
Dedicated IPs resource — provision, list, get, assign, release.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Union
from urllib.parse import quote

from .._client import AsyncHttpClient, HttpClient
from .._types import (
    AssignIpParams,
    DedicatedIp,
    DeleteResponse,
    IpAssignment,
    PaginatedResponse,
    PaginationParams,
    ProvisionDedicatedIpParams,
)


class DedicatedIps:
    """
    Synchronous dedicated IPs resource.

    Access via ``sendry.dedicated_ips``.
    """

    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def provision(
        self,
        params: Optional[Union[ProvisionDedicatedIpParams, Dict[str, Any]]] = None,
    ) -> DedicatedIp:
        """
        Provision a new dedicated IP address for email sending.

        Args:
            params: Optional dict with ``provider`` (``"ses"`` or ``"mailgun"``,
                defaults to ``"ses"``).

        Returns:
            The provisioned DedicatedIp.
        """
        return self._client.post("/v1/ips", dict(params) if params else {})

    def list(
        self, params: Optional[Union[PaginationParams, Dict[str, Any]]] = None
    ) -> PaginatedResponse:
        """List all dedicated IPs for your organisation."""
        return self._client.get("/v1/ips", dict(params) if params else None)

    def get(self, ip_id: str) -> DedicatedIp:
        """Get details for a specific dedicated IP."""
        return self._client.get(f"/v1/ips/{quote(ip_id, safe='')}")

    def assign(
        self, ip_id: str, params: Union[AssignIpParams, Dict[str, Any]]
    ) -> IpAssignment:
        """Assign a dedicated IP to a domain."""
        return self._client.post(
            f"/v1/ips/{quote(ip_id, safe='')}/assign", dict(params)
        )

    def remove_assignment(self, ip_id: str, assignment_id: str) -> DeleteResponse:
        """Remove a dedicated IP assignment from a domain."""
        return self._client.delete(
            f"/v1/ips/{quote(ip_id, safe='')}/assign/{quote(assignment_id, safe='')}"
        )

    def release(self, ip_id: str) -> DeleteResponse:
        """Release a dedicated IP address."""
        return self._client.delete(f"/v1/ips/{quote(ip_id, safe='')}")


class AsyncDedicatedIps:
    """
    Asynchronous dedicated IPs resource.

    Access via ``async_sendr.dedicated_ips``.
    """

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def provision(
        self,
        params: Optional[Union[ProvisionDedicatedIpParams, Dict[str, Any]]] = None,
    ) -> DedicatedIp:
        """Provision a dedicated IP. See :meth:`DedicatedIps.provision`."""
        return await self._client.post("/v1/ips", dict(params) if params else {})

    async def list(
        self, params: Optional[Union[PaginationParams, Dict[str, Any]]] = None
    ) -> PaginatedResponse:
        """List dedicated IPs. See :meth:`DedicatedIps.list`."""
        return await self._client.get("/v1/ips", dict(params) if params else None)

    async def get(self, ip_id: str) -> DedicatedIp:
        """Get a dedicated IP. See :meth:`DedicatedIps.get`."""
        return await self._client.get(f"/v1/ips/{quote(ip_id, safe='')}")

    async def assign(
        self, ip_id: str, params: Union[AssignIpParams, Dict[str, Any]]
    ) -> IpAssignment:
        """Assign a dedicated IP. See :meth:`DedicatedIps.assign`."""
        return await self._client.post(
            f"/v1/ips/{quote(ip_id, safe='')}/assign", dict(params)
        )

    async def remove_assignment(
        self, ip_id: str, assignment_id: str
    ) -> DeleteResponse:
        """Remove an IP assignment. See :meth:`DedicatedIps.remove_assignment`."""
        return await self._client.delete(
            f"/v1/ips/{quote(ip_id, safe='')}/assign/{quote(assignment_id, safe='')}"
        )

    async def release(self, ip_id: str) -> DeleteResponse:
        """Release a dedicated IP. See :meth:`DedicatedIps.release`."""
        return await self._client.delete(f"/v1/ips/{quote(ip_id, safe='')}")


__all__ = ["DedicatedIps", "AsyncDedicatedIps"]
