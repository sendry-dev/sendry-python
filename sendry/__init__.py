"""
Sendry Python SDK

The official Python client for the Sendry email API.

Quick start::

    from sendry import Sendry

    sendry = Sendry("sn_live_your_api_key")

    response = sendry.emails.send({
        "from_": "hello@yourdomain.com",
        "to": "user@example.com",
        "subject": "Hello from Sendry!",
        "html": "<p>Your email, delivered.</p>",
    })
    print(response["id"])

Async quick start::

    import asyncio
    from sendry import AsyncSendry

    async def main():
        client = AsyncSendry("sn_live_your_api_key")
        response = await client.emails.send({
            "from_": "hello@yourdomain.com",
            "to": "user@example.com",
            "subject": "Hello!",
            "html": "<p>World</p>",
        })
        print(response["id"])

    asyncio.run(main())
"""

from __future__ import annotations

from typing import Dict, Optional

from ._client import AsyncHttpClient, HttpClient
from ._exceptions import (
    ApiError,
    AuthenticationError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    SendryError,
    ValidationError,
)
from .resources.analytics import Analytics, AsyncAnalytics
from .resources.api_keys import ApiKeys, AsyncApiKeys
from .resources.audiences import AsyncAudiences, Audiences
from .resources.billing import AsyncBilling, Billing
from .resources.campaigns import AsyncCampaigns, Campaigns
from .resources.contacts import AsyncContacts, Contacts
from .resources.domains import AsyncDomains, Domains
from .resources.emails import AsyncEmails, Emails
from .resources.suppression import AsyncSuppression, Suppression
from .resources.team import AsyncTeam, Team
from .resources.templates import AsyncTemplates, Templates
from .resources.unsubscribes import AsyncUnsubscribes, Unsubscribes
from .resources.webhooks import AsyncWebhooks, Webhooks
from .resources.webhooks_util import verify_signature

__version__ = "0.1.0"

__all__ = [
    # Main client classes
    "Sendry",
    "AsyncSendry",
    # Exceptions
    "SendryError",
    "ApiError",
    "AuthenticationError",
    "ValidationError",
    "RateLimitError",
    "NotFoundError",
    "NetworkError",
    # Utilities
    "verify_signature",
    # Version
    "__version__",
]


class Sendry:
    """
    Synchronous Sendry API client.

    All resource groups are available as attributes on the client instance.

    Args:
        api_key: Your Sendry API key (e.g. ``sn_live_...`` or ``sn_test_...``).
        base_url: Override the default API base URL. Defaults to
            ``https://api.sendry.dev``.
        timeout: Request timeout in seconds. Defaults to 30.
        retries: Number of retries for 5xx and network errors.
            Defaults to 3 (delays: 1s, 2s, 4s).
        default_headers: Additional headers merged into every request.

    Example::

        # Simple
        sendry = Sendry("sn_live_abc123")

        # With options
        sendry = Sendry(
            api_key="sn_live_abc123",
            timeout=60,
            retries=2,
        )
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = "https://api.sendry.dev",
        timeout: float = 30.0,
        retries: int = 3,
        default_headers: Optional[Dict[str, str]] = None,
    ) -> None:
        client = HttpClient(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            retries=retries,
            default_headers=default_headers,
        )

        self.emails = Emails(client)
        self.domains = Domains(client)
        self.templates = Templates(client)
        self.api_keys = ApiKeys(client)
        self.webhooks = Webhooks(client)
        self.analytics = Analytics(client)
        self.suppression = Suppression(client)
        self.unsubscribes = Unsubscribes(client)
        self.contacts = Contacts(client)
        self.audiences = Audiences(client)
        self.campaigns = Campaigns(client)
        self.billing = Billing(client)
        self.team = Team(client)


class AsyncSendry:
    """
    Asynchronous Sendry API client.

    All resource groups are available as attributes on the client instance,
    and every method is a coroutine (``async def``).

    Args:
        api_key: Your Sendry API key (e.g. ``sn_live_...`` or ``sn_test_...``).
        base_url: Override the default API base URL. Defaults to
            ``https://api.sendry.dev``.
        timeout: Request timeout in seconds. Defaults to 30.
        retries: Number of retries for 5xx and network errors.
            Defaults to 3 (delays: 1s, 2s, 4s).
        default_headers: Additional headers merged into every request.

    Example::

        import asyncio
        from sendry import AsyncSendry

        async def main():
            client = AsyncSendry("sn_live_abc123")
            email = await client.emails.send({
                "from_": "hello@example.com",
                "to": "user@example.com",
                "subject": "Hi",
                "html": "<p>Hello</p>",
            })
            print(email["id"])

        asyncio.run(main())
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = "https://api.sendry.dev",
        timeout: float = 30.0,
        retries: int = 3,
        default_headers: Optional[Dict[str, str]] = None,
    ) -> None:
        client = AsyncHttpClient(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            retries=retries,
            default_headers=default_headers,
        )

        self.emails = AsyncEmails(client)
        self.domains = AsyncDomains(client)
        self.templates = AsyncTemplates(client)
        self.api_keys = AsyncApiKeys(client)
        self.webhooks = AsyncWebhooks(client)
        self.analytics = AsyncAnalytics(client)
        self.suppression = AsyncSuppression(client)
        self.unsubscribes = AsyncUnsubscribes(client)
        self.contacts = AsyncContacts(client)
        self.audiences = AsyncAudiences(client)
        self.campaigns = AsyncCampaigns(client)
        self.billing = AsyncBilling(client)
        self.team = AsyncTeam(client)
