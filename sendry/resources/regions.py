"""
Regions resource — list SES regions and configure org/domain region settings.
"""

from __future__ import annotations

from typing import Any, Dict, List, Union
from urllib.parse import quote

from .._client import AsyncHttpClient, HttpClient
from .._types import (
    OrgRegionSettings,
    Region,
    RegionAnalyticsParams,
    RegionAnalyticsResponse,
    UpdateDomainRegionParams,
    UpdateOrgRegionParams,
)


class Regions:
    """
    Synchronous regions resource.

    Access via ``sendry.regions``.
    """

    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def list(self) -> Dict[str, List[Region]]:
        """List all active SES regions available for sending."""
        return self._client.get("/v1/regions")

    def get_org_settings(self) -> OrgRegionSettings:
        """Get the org-level default SES sending region."""
        return self._client.get("/v1/organizations/me/region")

    def update_org_settings(
        self, params: Union[UpdateOrgRegionParams, Dict[str, Any]]
    ) -> OrgRegionSettings:
        """Update org-level default SES sending region and data residency."""
        return self._client.patch("/v1/organizations/me/region", dict(params))

    def set_domain_region(
        self,
        domain_id: str,
        params: Union[UpdateDomainRegionParams, Dict[str, Any]],
    ) -> Any:
        """Override the SES sending region for a specific domain."""
        return self._client.patch(
            f"/v1/domains/{quote(domain_id, safe='')}/region", dict(params)
        )

    def get_region_analytics(
        self, params: Union[RegionAnalyticsParams, Dict[str, Any]]
    ) -> RegionAnalyticsResponse:
        """Get a breakdown of sent emails by SES region for a date range."""
        return self._client.get("/v1/analytics/regions", dict(params))


class AsyncRegions:
    """
    Asynchronous regions resource.

    Access via ``async_sendr.regions``.
    """

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def list(self) -> Dict[str, List[Region]]:
        """List SES regions. See :meth:`Regions.list`."""
        return await self._client.get("/v1/regions")

    async def get_org_settings(self) -> OrgRegionSettings:
        """Get org region settings. See :meth:`Regions.get_org_settings`."""
        return await self._client.get("/v1/organizations/me/region")

    async def update_org_settings(
        self, params: Union[UpdateOrgRegionParams, Dict[str, Any]]
    ) -> OrgRegionSettings:
        """Update org region. See :meth:`Regions.update_org_settings`."""
        return await self._client.patch("/v1/organizations/me/region", dict(params))

    async def set_domain_region(
        self,
        domain_id: str,
        params: Union[UpdateDomainRegionParams, Dict[str, Any]],
    ) -> Any:
        """Set domain region. See :meth:`Regions.set_domain_region`."""
        return await self._client.patch(
            f"/v1/domains/{quote(domain_id, safe='')}/region", dict(params)
        )

    async def get_region_analytics(
        self, params: Union[RegionAnalyticsParams, Dict[str, Any]]
    ) -> RegionAnalyticsResponse:
        """Get region analytics. See :meth:`Regions.get_region_analytics`."""
        return await self._client.get("/v1/analytics/regions", dict(params))


__all__ = ["Regions", "AsyncRegions"]
