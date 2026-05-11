"""
Emails resource — send, retrieve, list, batch, marketing, cancel.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Union
from urllib.parse import quote

from .._client import AsyncHttpClient, HttpClient
from .._types import (
    BatchEmailResponse,
    CancelEmailResponse,
    Email,
    ListEmailsParams,
    PaginatedResponse,
    SendBatchParams,
    SendEmailParams,
    SendEmailResponse,
    SendMarketingEmailParams,
)


def _normalise_send_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """Map Python-friendly ``from_`` key back to the JSON ``from`` key."""
    out = dict(params)
    if "from_" in out:
        out["from"] = out.pop("from_")
    return out


class Emails:
    """
    Synchronous emails resource.

    Access via ``sendry.emails``.
    """

    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def send(self, params: Union[SendEmailParams, Dict[str, Any]]) -> SendEmailResponse:
        """
        Send a single transactional email.

        Args:
            params: Email parameters. Use ``from_`` for the sender address
                (it maps to the ``from`` JSON field).

        Returns:
            SendEmailResponse with the email ``id``, status, and metadata.

        Example::

            response = sendry.emails.send({
                "from_": "hello@example.com",
                "to": "user@example.com",
                "subject": "Hello!",
                "html": "<p>World</p>",
            })
            print(response["id"])
        """
        return self._client.post("/v1/emails", _normalise_send_params(dict(params)))

    def get(self, email_id: str) -> Email:
        """
        Get a single email by ID.

        Args:
            email_id: The email ID (e.g. ``em_abc123``).

        Returns:
            Full Email object including current status.

        Example::

            email = sendry.emails.get("em_abc123")
            print(email["status"])  # "delivered"
        """
        return self._client.get(f"/v1/emails/{quote(email_id, safe='')}")

    def list(self, params: Optional[Union[ListEmailsParams, Dict[str, Any]]] = None) -> PaginatedResponse:
        """
        List emails with cursor-based pagination.

        Args:
            params: Optional filters — ``status``, ``limit``, ``cursor``.

        Returns:
            PaginatedResponse containing ``data``, ``has_more``, ``next_cursor``.

        Example::

            page = sendry.emails.list({"limit": 25, "status": "delivered"})
            for email in page["data"]:
                print(email["id"])
        """
        return self._client.get("/v1/emails", dict(params) if params else None)

    def send_batch(self, params: Union[SendBatchParams, Dict[str, Any]]) -> BatchEmailResponse:
        """
        Send a batch of up to 100 emails in a single request.

        Args:
            params: Batch parameters with a shared ``from_``/``subject``
                and a list of per-email overrides.

        Returns:
            BatchEmailResponse with a list of ``{id, status}`` per email.

        Example::

            result = sendry.emails.send_batch({
                "from_": "hello@example.com",
                "emails": [
                    {"to": "a@example.com", "subject": "Hi A", "html": "<p>A</p>"},
                    {"to": "b@example.com", "subject": "Hi B", "html": "<p>B</p>"},
                ],
            })
        """
        return self._client.post("/v1/emails/batch", _normalise_send_params(dict(params)))

    def send_marketing(
        self, params: Union[SendMarketingEmailParams, Dict[str, Any]]
    ) -> SendEmailResponse:
        """
        Send a marketing email with unsubscribe link support.

        Args:
            params: Marketing email parameters. Must include ``unsubscribe_url``.

        Returns:
            SendEmailResponse with the email ``id`` and metadata.

        Example::

            sendry.emails.send_marketing({
                "from_": "news@example.com",
                "to": "subscriber@example.com",
                "subject": "March Newsletter",
                "html": "<p>News!</p>",
                "unsubscribe_url": "https://example.com/unsub?token=abc",
            })
        """
        return self._client.post("/v1/emails/marketing", _normalise_send_params(dict(params)))

    def cancel(self, email_id: str) -> CancelEmailResponse:
        """
        Cancel a queued email before it is sent.

        Only emails in ``queued`` status can be cancelled.

        Args:
            email_id: The email ID.

        Returns:
            CancelEmailResponse with ``id`` and ``status`` set to ``"cancelled"``.

        Example::

            result = sendry.emails.cancel("em_abc123")
            print(result["status"])  # "cancelled"
        """
        return self._client.post(f"/v1/emails/{quote(email_id, safe='')}/cancel")


class AsyncEmails:
    """
    Asynchronous emails resource.

    Access via ``async_sendr.emails``.
    """

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def send(self, params: Union[SendEmailParams, Dict[str, Any]]) -> SendEmailResponse:
        """Send a single transactional email. See :meth:`Emails.send`."""
        return await self._client.post("/v1/emails", _normalise_send_params(dict(params)))

    async def get(self, email_id: str) -> Email:
        """Get a single email by ID. See :meth:`Emails.get`."""
        return await self._client.get(f"/v1/emails/{quote(email_id, safe='')}")

    async def list(
        self, params: Optional[Union[ListEmailsParams, Dict[str, Any]]] = None
    ) -> PaginatedResponse:
        """List emails with cursor-based pagination. See :meth:`Emails.list`."""
        return await self._client.get("/v1/emails", dict(params) if params else None)

    async def send_batch(
        self, params: Union[SendBatchParams, Dict[str, Any]]
    ) -> BatchEmailResponse:
        """Send a batch of emails. See :meth:`Emails.send_batch`."""
        return await self._client.post("/v1/emails/batch", _normalise_send_params(dict(params)))

    async def send_marketing(
        self, params: Union[SendMarketingEmailParams, Dict[str, Any]]
    ) -> SendEmailResponse:
        """Send a marketing email. See :meth:`Emails.send_marketing`."""
        return await self._client.post(
            "/v1/emails/marketing", _normalise_send_params(dict(params))
        )

    async def cancel(self, email_id: str) -> CancelEmailResponse:
        """Cancel a queued email. See :meth:`Emails.cancel`."""
        return await self._client.post(f"/v1/emails/{quote(email_id, safe='')}/cancel")


__all__ = ["Emails", "AsyncEmails"]
