"""
API Keys resource — create, list, remove.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Union
from urllib.parse import quote

from .._client import AsyncHttpClient, HttpClient
from .._types import (
    ApiKey,
    ApiKeyCreated,
    CreateApiKeyParams,
    DeleteResponse,
    PaginatedResponse,
    PaginationParams,
)


class ApiKeys:
    """
    Synchronous API keys resource.

    Access via ``sendry.api_keys``.
    """

    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def create(self, params: Union[CreateApiKeyParams, Dict[str, Any]]) -> ApiKeyCreated:
        """
        Create a new API key.

        The full key value is included in the response exactly once and cannot
        be retrieved again. Store it securely immediately after creation.

        Args:
            params: Must include ``name``. Optionally specify ``scope``
                (``"full_access"``, ``"sending_access"``, or ``"read_only"``).

        Returns:
            ApiKeyCreated with the plaintext ``key`` field.

        Example::

            result = sendry.api_keys.create({
                "name": "Production Key",
                "scope": "sending_access",
            })
            # Store result["key"] securely — it cannot be retrieved again
            print(result["key"])
        """
        return self._client.post("/v1/api-keys", dict(params))

    def list(self, params: Optional[Union[PaginationParams, Dict[str, Any]]] = None) -> PaginatedResponse:
        """
        List all API keys.

        Key values are masked — only the prefix is shown.

        Args:
            params: Optional ``limit`` and ``cursor`` for pagination.

        Returns:
            PaginatedResponse of ApiKey objects.
        """
        return self._client.get("/v1/api-keys", dict(params) if params else None)

    def remove(self, key_id: str) -> DeleteResponse:
        """
        Revoke (delete) an API key.

        Revoking a key immediately invalidates it. Any requests using the
        revoked key will receive a 401 response.

        Args:
            key_id: The API key ID (e.g. ``ak_abc123``).

        Returns:
            DeleteResponse acknowledging the revocation.

        Example::

            sendry.api_keys.remove("ak_abc123")
        """
        return self._client.delete(f"/v1/api-keys/{quote(key_id, safe='')}")


class AsyncApiKeys:
    """
    Asynchronous API keys resource.

    Access via ``async_sendr.api_keys``.
    """

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def create(self, params: Union[CreateApiKeyParams, Dict[str, Any]]) -> ApiKeyCreated:
        """Create an API key. See :meth:`ApiKeys.create`."""
        return await self._client.post("/v1/api-keys", dict(params))

    async def list(
        self, params: Optional[Union[PaginationParams, Dict[str, Any]]] = None
    ) -> PaginatedResponse:
        """List API keys. See :meth:`ApiKeys.list`."""
        return await self._client.get("/v1/api-keys", dict(params) if params else None)

    async def remove(self, key_id: str) -> DeleteResponse:
        """Revoke an API key. See :meth:`ApiKeys.remove`."""
        return await self._client.delete(f"/v1/api-keys/{quote(key_id, safe='')}")


__all__ = ["ApiKeys", "AsyncApiKeys"]
