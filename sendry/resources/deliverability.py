"""
Deliverability resource — reputation, blocklist, and report queries.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Union
from urllib.parse import quote

from .._client import AsyncHttpClient, HttpClient
from .._types import (
    BlocklistCheckBody,
    BlocklistQuery,
    BlocklistResponse,
    DeliverabilityReport,
    DeliverabilityReportQuery,
    ReputationHistoryQuery,
    ReputationQuery,
    ReputationResponse,
)


class Deliverability:
    """
    Synchronous deliverability resource.

    Access via ``sendry.deliverability``.
    """

    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def get_reputation(
        self, params: Optional[Union[ReputationQuery, Dict[str, Any]]] = None
    ) -> ReputationResponse:
        """Get a reputation overview for your org or a specific domain."""
        return self._client.get(
            "/v1/deliverability/reputation", dict(params) if params else None
        )

    def get_reputation_history(
        self,
        domain_id: str,
        params: Optional[Union[ReputationHistoryQuery, Dict[str, Any]]] = None,
    ) -> Any:
        """Get reputation score history for a specific domain."""
        return self._client.get(
            f"/v1/deliverability/reputation/{quote(domain_id, safe='')}/history",
            dict(params) if params else None,
        )

    def get_blocklist(
        self, params: Optional[Union[BlocklistQuery, Dict[str, Any]]] = None
    ) -> BlocklistResponse:
        """Get blocklist status for your domains and IPs."""
        return self._client.get(
            "/v1/deliverability/blocklist", dict(params) if params else None
        )

    def run_blocklist_check(
        self, params: Union[BlocklistCheckBody, Dict[str, Any]]
    ) -> Any:
        """Run an on-demand blocklist check."""
        return self._client.post("/v1/deliverability/blocklist/check", dict(params))

    def dismiss_alert(self, alert_id: str) -> Any:
        """Dismiss a blocklist alert by ID."""
        return self._client.patch(
            f"/v1/deliverability/blocklist/alerts/{quote(alert_id, safe='')}",
            {"status": "dismissed"},
        )

    def get_report(
        self,
        params: Optional[Union[DeliverabilityReportQuery, Dict[str, Any]]] = None,
    ) -> DeliverabilityReport:
        """Get a comprehensive deliverability report for a date range."""
        return self._client.get(
            "/v1/deliverability/report", dict(params) if params else None
        )


class AsyncDeliverability:
    """
    Asynchronous deliverability resource.

    Access via ``async_sendr.deliverability``.
    """

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def get_reputation(
        self, params: Optional[Union[ReputationQuery, Dict[str, Any]]] = None
    ) -> ReputationResponse:
        """Get reputation overview. See :meth:`Deliverability.get_reputation`."""
        return await self._client.get(
            "/v1/deliverability/reputation", dict(params) if params else None
        )

    async def get_reputation_history(
        self,
        domain_id: str,
        params: Optional[Union[ReputationHistoryQuery, Dict[str, Any]]] = None,
    ) -> Any:
        """Get reputation history. See :meth:`Deliverability.get_reputation_history`."""
        return await self._client.get(
            f"/v1/deliverability/reputation/{quote(domain_id, safe='')}/history",
            dict(params) if params else None,
        )

    async def get_blocklist(
        self, params: Optional[Union[BlocklistQuery, Dict[str, Any]]] = None
    ) -> BlocklistResponse:
        """Get blocklist status. See :meth:`Deliverability.get_blocklist`."""
        return await self._client.get(
            "/v1/deliverability/blocklist", dict(params) if params else None
        )

    async def run_blocklist_check(
        self, params: Union[BlocklistCheckBody, Dict[str, Any]]
    ) -> Any:
        """Run blocklist check. See :meth:`Deliverability.run_blocklist_check`."""
        return await self._client.post(
            "/v1/deliverability/blocklist/check", dict(params)
        )

    async def dismiss_alert(self, alert_id: str) -> Any:
        """Dismiss alert. See :meth:`Deliverability.dismiss_alert`."""
        return await self._client.patch(
            f"/v1/deliverability/blocklist/alerts/{quote(alert_id, safe='')}",
            {"status": "dismissed"},
        )

    async def get_report(
        self,
        params: Optional[Union[DeliverabilityReportQuery, Dict[str, Any]]] = None,
    ) -> DeliverabilityReport:
        """Get deliverability report. See :meth:`Deliverability.get_report`."""
        return await self._client.get(
            "/v1/deliverability/report", dict(params) if params else None
        )


__all__ = ["Deliverability", "AsyncDeliverability"]
