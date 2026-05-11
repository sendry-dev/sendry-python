"""
Campaigns resource — create, list, get, update, remove, schedule, send, cancel, pause, resume.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Union
from urllib.parse import quote

from .._client import AsyncHttpClient, HttpClient
from .._types import (
    Campaign,
    CampaignActionResponse,
    CampaignListItem,
    CreateCampaignParams,
    DeleteResponse,
    ListCampaignsParams,
    PaginatedResponse,
    ScheduleCampaignParams,
    UpdateCampaignParams,
)


def _normalise_campaign_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """Map Python-friendly ``from_`` key back to the JSON ``from`` key."""
    out = dict(params)
    if "from_" in out:
        out["from"] = out.pop("from_")
    return out


class Campaigns:
    """
    Synchronous campaigns resource.

    Access via ``sendry.campaigns``.
    """

    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def create(self, params: Union[CreateCampaignParams, Dict[str, Any]]) -> Campaign:
        """
        Create a new email campaign in draft status.

        Args:
            params: Must include ``name``, ``subject``, ``from_``, and
                ``audience_id``. Optional: ``reply_to``, ``preview_text``,
                ``template_id``, ``html``, ``text``.

        Returns:
            Campaign object in ``draft`` status.

        Example::

            campaign = sendry.campaigns.create({
                "name": "March Newsletter",
                "subject": "What's new in March",
                "from_": "Acme <hello@acme.com>",
                "audience_id": "aud_abc123",
                "html": "<h1>Hello!</h1>",
            })
            print(campaign["id"])
        """
        return self._client.post("/v1/campaigns", _normalise_campaign_params(dict(params)))

    def list(
        self, params: Optional[Union[ListCampaignsParams, Dict[str, Any]]] = None
    ) -> PaginatedResponse:
        """
        List all campaigns with cursor-based pagination.

        Args:
            params: Optional filters — ``status``, ``cursor``, ``limit``.

        Returns:
            PaginatedResponse of CampaignListItem objects.

        Example::

            drafts = sendry.campaigns.list({"status": "draft"})
        """
        return self._client.get("/v1/campaigns", dict(params) if params else None)

    def get(self, campaign_id: str) -> Campaign:
        """
        Get a campaign by ID including delivery statistics.

        Args:
            campaign_id: The campaign ID (e.g. ``cp_abc123``).

        Returns:
            Full Campaign object with ``stats``.

        Example::

            campaign = sendry.campaigns.get("cp_abc123")
            print(f"Delivered: {campaign['stats']['delivered_count']}")
        """
        return self._client.get(f"/v1/campaigns/{quote(campaign_id, safe='')}")

    def update(
        self, campaign_id: str, params: Union[UpdateCampaignParams, Dict[str, Any]]
    ) -> Campaign:
        """
        Update a campaign. Only ``draft`` campaigns can be updated.

        Args:
            campaign_id: The campaign ID.
            params: Fields to update. Use ``from_`` for the sender address.

        Returns:
            Updated Campaign object.

        Example::

            updated = sendry.campaigns.update("cp_abc123", {
                "subject": "Updated subject line",
            })
        """
        return self._client.put(
            f"/v1/campaigns/{quote(campaign_id, safe='')}",
            _normalise_campaign_params(dict(params)),
        )

    def remove(self, campaign_id: str) -> DeleteResponse:
        """
        Delete a campaign.

        Only ``draft`` or ``cancelled`` campaigns can be deleted.

        Args:
            campaign_id: The campaign ID.

        Returns:
            DeleteResponse acknowledging the deletion.
        """
        return self._client.delete(f"/v1/campaigns/{quote(campaign_id, safe='')}")

    def schedule(
        self, campaign_id: str, params: Union[ScheduleCampaignParams, Dict[str, Any]]
    ) -> CampaignActionResponse:
        """
        Schedule a draft campaign to send at a specific time.

        Args:
            campaign_id: The campaign ID.
            params: Must include ``scheduled_at`` as an ISO 8601 datetime string.

        Returns:
            CampaignActionResponse with updated ``status`` (``"scheduled"``).

        Example::

            sendry.campaigns.schedule("cp_abc123", {
                "scheduled_at": "2026-03-15T10:00:00Z",
            })
        """
        return self._client.post(
            f"/v1/campaigns/{quote(campaign_id, safe='')}/schedule", dict(params)
        )

    def send(self, campaign_id: str) -> CampaignActionResponse:
        """
        Immediately send a draft or scheduled campaign.

        Args:
            campaign_id: The campaign ID.

        Returns:
            CampaignActionResponse with ``status`` set to ``"sending"``.

        Example::

            sendry.campaigns.send("cp_abc123")
        """
        return self._client.post(f"/v1/campaigns/{quote(campaign_id, safe='')}/send")

    def cancel(self, campaign_id: str) -> CampaignActionResponse:
        """
        Cancel a scheduled or paused campaign.

        Args:
            campaign_id: The campaign ID.

        Returns:
            CampaignActionResponse with ``status`` set to ``"cancelled"``.
        """
        return self._client.post(f"/v1/campaigns/{quote(campaign_id, safe='')}/cancel")

    def pause(self, campaign_id: str) -> CampaignActionResponse:
        """
        Pause a campaign that is currently sending.

        Args:
            campaign_id: The campaign ID.

        Returns:
            CampaignActionResponse with ``status`` set to ``"paused"``.
        """
        return self._client.post(f"/v1/campaigns/{quote(campaign_id, safe='')}/pause")

    def resume(self, campaign_id: str) -> CampaignActionResponse:
        """
        Resume a paused campaign.

        Args:
            campaign_id: The campaign ID.

        Returns:
            CampaignActionResponse with ``status`` set to ``"sending"``.
        """
        return self._client.post(f"/v1/campaigns/{quote(campaign_id, safe='')}/resume")


class AsyncCampaigns:
    """
    Asynchronous campaigns resource.

    Access via ``async_sendr.campaigns``.
    """

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def create(self, params: Union[CreateCampaignParams, Dict[str, Any]]) -> Campaign:
        """Create a campaign. See :meth:`Campaigns.create`."""
        return await self._client.post(
            "/v1/campaigns", _normalise_campaign_params(dict(params))
        )

    async def list(
        self, params: Optional[Union[ListCampaignsParams, Dict[str, Any]]] = None
    ) -> PaginatedResponse:
        """List campaigns. See :meth:`Campaigns.list`."""
        return await self._client.get("/v1/campaigns", dict(params) if params else None)

    async def get(self, campaign_id: str) -> Campaign:
        """Get a campaign. See :meth:`Campaigns.get`."""
        return await self._client.get(f"/v1/campaigns/{quote(campaign_id, safe='')}")

    async def update(
        self, campaign_id: str, params: Union[UpdateCampaignParams, Dict[str, Any]]
    ) -> Campaign:
        """Update a campaign. See :meth:`Campaigns.update`."""
        return await self._client.put(
            f"/v1/campaigns/{quote(campaign_id, safe='')}",
            _normalise_campaign_params(dict(params)),
        )

    async def remove(self, campaign_id: str) -> DeleteResponse:
        """Delete a campaign. See :meth:`Campaigns.remove`."""
        return await self._client.delete(f"/v1/campaigns/{quote(campaign_id, safe='')}")

    async def schedule(
        self, campaign_id: str, params: Union[ScheduleCampaignParams, Dict[str, Any]]
    ) -> CampaignActionResponse:
        """Schedule a campaign. See :meth:`Campaigns.schedule`."""
        return await self._client.post(
            f"/v1/campaigns/{quote(campaign_id, safe='')}/schedule", dict(params)
        )

    async def send(self, campaign_id: str) -> CampaignActionResponse:
        """Immediately send a campaign. See :meth:`Campaigns.send`."""
        return await self._client.post(f"/v1/campaigns/{quote(campaign_id, safe='')}/send")

    async def cancel(self, campaign_id: str) -> CampaignActionResponse:
        """Cancel a campaign. See :meth:`Campaigns.cancel`."""
        return await self._client.post(f"/v1/campaigns/{quote(campaign_id, safe='')}/cancel")

    async def pause(self, campaign_id: str) -> CampaignActionResponse:
        """Pause a campaign. See :meth:`Campaigns.pause`."""
        return await self._client.post(f"/v1/campaigns/{quote(campaign_id, safe='')}/pause")

    async def resume(self, campaign_id: str) -> CampaignActionResponse:
        """Resume a campaign. See :meth:`Campaigns.resume`."""
        return await self._client.post(f"/v1/campaigns/{quote(campaign_id, safe='')}/resume")


__all__ = ["Campaigns", "AsyncCampaigns"]
