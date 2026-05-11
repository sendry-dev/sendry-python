"""
Domains resource — create, list, get, verify, remove, and BIMI configuration.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Union
from urllib.parse import quote

from .._client import AsyncHttpClient, HttpClient
from .._types import (
    BimiConfig,
    ConfigureBimiParams,
    CreateDomainParams,
    DeleteResponse,
    Domain,
    PaginatedResponse,
    PaginationParams,
    VerifyBimiResponse,
    VerifyDomainResponse,
)


class Domains:
    """
    Synchronous domains resource.

    Access via ``sendry.domains``.
    """

    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def create(self, params: Union[CreateDomainParams, Dict[str, Any]]) -> Domain:
        """
        Add a sending domain to your account.

        After creating a domain, add the returned ``dns_records`` to your
        DNS provider, then call :meth:`verify` to confirm ownership.

        Args:
            params: Must contain ``name`` (e.g. ``"mail.example.com"``).

        Returns:
            Domain object with DNS records to configure.

        Example::

            domain = sendry.domains.create({"name": "mail.example.com"})
            for record in domain["dns_records"]:
                print(record["type"], record["host"], record["value"])
        """
        return self._client.post("/v1/domains", dict(params))

    def list(self, params: Optional[Union[PaginationParams, Dict[str, Any]]] = None) -> PaginatedResponse:
        """
        List all domains.

        Args:
            params: Optional ``limit`` and ``cursor`` for pagination.

        Returns:
            PaginatedResponse of Domain objects.
        """
        return self._client.get("/v1/domains", dict(params) if params else None)

    def get(self, domain_id: str) -> Domain:
        """
        Get a domain by ID.

        Args:
            domain_id: The domain ID (e.g. ``dom_abc123``).

        Returns:
            Domain object including current verification status.
        """
        return self._client.get(f"/v1/domains/{quote(domain_id, safe='')}")

    def verify(self, domain_id: str) -> VerifyDomainResponse:
        """
        Trigger DNS verification for a domain.

        Args:
            domain_id: The domain ID.

        Returns:
            Verification result with per-record status flags.

        Example::

            result = sendry.domains.verify("dom_abc123")
            if result["spf_verified"] and result["dkim_verified"]:
                print("Domain is fully verified!")
        """
        return self._client.post(f"/v1/domains/{quote(domain_id, safe='')}/verify")

    def remove(self, domain_id: str) -> DeleteResponse:
        """
        Delete a domain and its DNS records from your account.

        Args:
            domain_id: The domain ID.

        Returns:
            DeleteResponse acknowledging the deletion.
        """
        return self._client.delete(f"/v1/domains/{quote(domain_id, safe='')}")

    def configure_bimi(
        self, domain_id: str, params: Union[ConfigureBimiParams, Dict[str, Any]]
    ) -> BimiConfig:
        """
        Configure BIMI (Brand Indicators for Message Identification) for a domain.

        BIMI displays your logo next to emails in supporting mail clients.
        The ``logo_url`` must point to a publicly accessible SVG file.

        Args:
            domain_id: The domain ID.
            params: BIMI configuration — ``logo_url`` is required;
                ``vmc_url`` and ``selector`` are optional.

        Returns:
            BimiConfig object with DNS record instructions.

        Example::

            bimi = sendry.domains.configure_bimi("dom_abc123", {
                "logo_url": "https://example.com/logo.svg",
                "vmc_url": "https://example.com/vmc.pem",
            })
        """
        return self._client.post(
            f"/v1/domains/{quote(domain_id, safe='')}/bimi", dict(params)
        )

    def get_bimi(self, domain_id: str) -> BimiConfig:
        """
        Get the BIMI configuration for a domain.

        Args:
            domain_id: The domain ID.

        Returns:
            BimiConfig object.

        Raises:
            NotFoundError: If BIMI has not been configured for this domain.
        """
        return self._client.get(f"/v1/domains/{quote(domain_id, safe='')}/bimi")

    def verify_bimi(self, domain_id: str) -> VerifyBimiResponse:
        """
        Trigger DNS verification for the BIMI TXT record.

        Args:
            domain_id: The domain ID.

        Returns:
            VerifyBimiResponse with ``verified`` flag and current status.
        """
        return self._client.post(f"/v1/domains/{quote(domain_id, safe='')}/bimi/verify")

    def remove_bimi(self, domain_id: str) -> DeleteResponse:
        """
        Remove the BIMI configuration from a domain.

        Args:
            domain_id: The domain ID.

        Returns:
            DeleteResponse acknowledging the deletion.
        """
        return self._client.delete(f"/v1/domains/{quote(domain_id, safe='')}/bimi")


class AsyncDomains:
    """
    Asynchronous domains resource.

    Access via ``async_sendr.domains``.
    """

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def create(self, params: Union[CreateDomainParams, Dict[str, Any]]) -> Domain:
        """Add a sending domain. See :meth:`Domains.create`."""
        return await self._client.post("/v1/domains", dict(params))

    async def list(
        self, params: Optional[Union[PaginationParams, Dict[str, Any]]] = None
    ) -> PaginatedResponse:
        """List all domains. See :meth:`Domains.list`."""
        return await self._client.get("/v1/domains", dict(params) if params else None)

    async def get(self, domain_id: str) -> Domain:
        """Get a domain by ID. See :meth:`Domains.get`."""
        return await self._client.get(f"/v1/domains/{quote(domain_id, safe='')}")

    async def verify(self, domain_id: str) -> VerifyDomainResponse:
        """Trigger DNS verification. See :meth:`Domains.verify`."""
        return await self._client.post(f"/v1/domains/{quote(domain_id, safe='')}/verify")

    async def remove(self, domain_id: str) -> DeleteResponse:
        """Delete a domain. See :meth:`Domains.remove`."""
        return await self._client.delete(f"/v1/domains/{quote(domain_id, safe='')}")

    async def configure_bimi(
        self, domain_id: str, params: Union[ConfigureBimiParams, Dict[str, Any]]
    ) -> BimiConfig:
        """Configure BIMI. See :meth:`Domains.configure_bimi`."""
        return await self._client.post(
            f"/v1/domains/{quote(domain_id, safe='')}/bimi", dict(params)
        )

    async def get_bimi(self, domain_id: str) -> BimiConfig:
        """Get BIMI config. See :meth:`Domains.get_bimi`."""
        return await self._client.get(f"/v1/domains/{quote(domain_id, safe='')}/bimi")

    async def verify_bimi(self, domain_id: str) -> VerifyBimiResponse:
        """Verify BIMI record. See :meth:`Domains.verify_bimi`."""
        return await self._client.post(f"/v1/domains/{quote(domain_id, safe='')}/bimi/verify")

    async def remove_bimi(self, domain_id: str) -> DeleteResponse:
        """Remove BIMI config. See :meth:`Domains.remove_bimi`."""
        return await self._client.delete(f"/v1/domains/{quote(domain_id, safe='')}/bimi")


__all__ = ["Domains", "AsyncDomains"]
