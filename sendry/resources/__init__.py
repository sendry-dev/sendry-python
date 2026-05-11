"""Resource classes for the Sendry Python SDK."""

from .analytics import Analytics, AsyncAnalytics
from .api_keys import ApiKeys, AsyncApiKeys
from .audiences import AsyncAudiences, Audiences
from .billing import AsyncBilling, Billing
from .campaigns import AsyncCampaigns, Campaigns
from .contacts import AsyncContacts, Contacts
from .domains import AsyncDomains, Domains
from .emails import AsyncEmails, Emails
from .suppression import AsyncSuppression, Suppression
from .team import AsyncTeam, Team
from .templates import AsyncTemplates, Templates
from .unsubscribes import AsyncUnsubscribes, Unsubscribes
from .webhooks import AsyncWebhooks, Webhooks
from .webhooks_util import verify_signature

__all__ = [
    "Analytics",
    "AsyncAnalytics",
    "ApiKeys",
    "AsyncApiKeys",
    "Audiences",
    "AsyncAudiences",
    "Billing",
    "AsyncBilling",
    "Campaigns",
    "AsyncCampaigns",
    "Contacts",
    "AsyncContacts",
    "Domains",
    "AsyncDomains",
    "Emails",
    "AsyncEmails",
    "Suppression",
    "AsyncSuppression",
    "Team",
    "AsyncTeam",
    "Templates",
    "AsyncTemplates",
    "Unsubscribes",
    "AsyncUnsubscribes",
    "Webhooks",
    "AsyncWebhooks",
    "verify_signature",
]
