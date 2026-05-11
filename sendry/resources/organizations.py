"""
Organizations resource — current org details and branding settings.
"""

from __future__ import annotations

from typing import Any, Dict, Union

from .._client import AsyncHttpClient, HttpClient
from .._types import (
    BrandingSettings,
    Organization,
    UpdateBrandingParams,
    UpdateOrganizationParams,
)


class Organizations:
    """
    Synchronous organizations resource.

    Access via ``sendry.organizations``.
    """

    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def get_current(self) -> Organization:
        """Get the current organisation's details."""
        return self._client.get("/v1/organizations/me")

    def update(
        self, params: Union[UpdateOrganizationParams, Dict[str, Any]]
    ) -> Organization:
        """Update the current organisation's name."""
        return self._client.patch("/v1/organizations/me", dict(params))

    def get_branding(self) -> BrandingSettings:
        """Get the current organisation's branding settings."""
        return self._client.get("/v1/organizations/me/branding")

    def update_branding(
        self, params: Union[UpdateBrandingParams, Dict[str, Any]]
    ) -> BrandingSettings:
        """Update the current organisation's branding settings."""
        return self._client.patch("/v1/organizations/me/branding", dict(params))


class AsyncOrganizations:
    """
    Asynchronous organizations resource.

    Access via ``async_sendr.organizations``.
    """

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def get_current(self) -> Organization:
        """Get current org. See :meth:`Organizations.get_current`."""
        return await self._client.get("/v1/organizations/me")

    async def update(
        self, params: Union[UpdateOrganizationParams, Dict[str, Any]]
    ) -> Organization:
        """Update current org. See :meth:`Organizations.update`."""
        return await self._client.patch("/v1/organizations/me", dict(params))

    async def get_branding(self) -> BrandingSettings:
        """Get branding. See :meth:`Organizations.get_branding`."""
        return await self._client.get("/v1/organizations/me/branding")

    async def update_branding(
        self, params: Union[UpdateBrandingParams, Dict[str, Any]]
    ) -> BrandingSettings:
        """Update branding. See :meth:`Organizations.update_branding`."""
        return await self._client.patch("/v1/organizations/me/branding", dict(params))


__all__ = ["Organizations", "AsyncOrganizations"]
