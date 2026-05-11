"""
Webhooks resource — create, list, get, update, remove.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Union
from urllib.parse import quote

from .._client import AsyncHttpClient, HttpClient
from .._types import (
    CreateWebhookParams,
    DeleteResponse,
    PaginatedResponse,
    PaginationParams,
    UpdateWebhookParams,
    Webhook,
    WebhookListItem,
)


class Webhooks:
    """
    Synchronous webhooks resource.

    Access via ``sendry.webhooks``.
    """

    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def create(self, params: Union[CreateWebhookParams, Dict[str, Any]]) -> Webhook:
        """
        Create a webhook endpoint.

        The response includes a ``secret`` for verifying webhook payloads
        using HMAC-SHA256. Use :func:`sendry.webhooks_util.verify_signature`
        to validate incoming requests.

        Args:
            params: Must include ``url`` and ``events`` list.
                Common events: ``email.delivered``, ``email.bounced``,
                ``email.opened``, ``email.clicked``, ``email.complained``.

        Returns:
            Webhook object including the signing ``secret``.

        Example::

            webhook = sendry.webhooks.create({
                "url": "https://example.com/webhooks/sendry",
                "events": ["email.delivered", "email.bounced"],
            })
            # Store webhook["secret"] securely
        """
        return self._client.post("/v1/webhooks", dict(params))

    def list(self, params: Optional[Union[PaginationParams, Dict[str, Any]]] = None) -> PaginatedResponse:
        """
        List all webhook endpoints.

        Args:
            params: Optional ``limit`` and ``cursor`` for pagination.

        Returns:
            PaginatedResponse of WebhookListItem objects (no ``secret`` field).
        """
        return self._client.get("/v1/webhooks", dict(params) if params else None)

    def get(self, webhook_id: str) -> Webhook:
        """
        Get a webhook by ID, including its signing secret.

        Args:
            webhook_id: The webhook ID (e.g. ``wh_abc123``).

        Returns:
            Full Webhook object including the ``secret``.
        """
        return self._client.get(f"/v1/webhooks/{quote(webhook_id, safe='')}")

    def update(
        self, webhook_id: str, params: Union[UpdateWebhookParams, Dict[str, Any]]
    ) -> Webhook:
        """
        Update a webhook's URL, events, or active state.

        Args:
            webhook_id: The webhook ID.
            params: Fields to update. All are optional.

        Returns:
            Updated Webhook object.

        Example::

            sendry.webhooks.update("wh_abc123", {
                "events": ["email.delivered"],
                "active": False,
            })
        """
        return self._client.put(f"/v1/webhooks/{quote(webhook_id, safe='')}", dict(params))

    def remove(self, webhook_id: str) -> DeleteResponse:
        """
        Delete a webhook endpoint.

        Args:
            webhook_id: The webhook ID.

        Returns:
            DeleteResponse acknowledging the deletion.
        """
        return self._client.delete(f"/v1/webhooks/{quote(webhook_id, safe='')}")


class AsyncWebhooks:
    """
    Asynchronous webhooks resource.

    Access via ``async_sendr.webhooks``.
    """

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def create(self, params: Union[CreateWebhookParams, Dict[str, Any]]) -> Webhook:
        """Create a webhook. See :meth:`Webhooks.create`."""
        return await self._client.post("/v1/webhooks", dict(params))

    async def list(
        self, params: Optional[Union[PaginationParams, Dict[str, Any]]] = None
    ) -> PaginatedResponse:
        """List webhooks. See :meth:`Webhooks.list`."""
        return await self._client.get("/v1/webhooks", dict(params) if params else None)

    async def get(self, webhook_id: str) -> Webhook:
        """Get a webhook. See :meth:`Webhooks.get`."""
        return await self._client.get(f"/v1/webhooks/{quote(webhook_id, safe='')}")

    async def update(
        self, webhook_id: str, params: Union[UpdateWebhookParams, Dict[str, Any]]
    ) -> Webhook:
        """Update a webhook. See :meth:`Webhooks.update`."""
        return await self._client.put(
            f"/v1/webhooks/{quote(webhook_id, safe='')}", dict(params)
        )

    async def remove(self, webhook_id: str) -> DeleteResponse:
        """Delete a webhook. See :meth:`Webhooks.remove`."""
        return await self._client.delete(f"/v1/webhooks/{quote(webhook_id, safe='')}")


__all__ = ["Webhooks", "AsyncWebhooks"]
