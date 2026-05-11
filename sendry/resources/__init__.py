"""Resource classes for the Sendry Python SDK."""

from .analytics import Analytics, AsyncAnalytics
from .api_keys import ApiKeys, AsyncApiKeys
from .audiences import AsyncAudiences, Audiences
from .automations import AsyncAutomations, Automations
from .billing import AsyncBilling, Billing
from .campaigns import AsyncCampaigns, Campaigns
from .contacts import AsyncContacts, Contacts
from .dedicated_ips import AsyncDedicatedIps, DedicatedIps
from .deliverability import AsyncDeliverability, Deliverability
from .domains import AsyncDomains, Domains
from .emails import AsyncEmails, Emails
from .events import AsyncEvents, Events
from .inbound import AsyncInbound, Inbound
from .notification_preferences import (
    AsyncNotificationPreferencesResource,
    NotificationPreferencesResource,
)
from .organizations import AsyncOrganizations, Organizations
from .regions import AsyncRegions, Regions
from .status import AsyncStatus, Status
from .suppression import AsyncSuppression, Suppression
from .team import AsyncTeam, Team
from .templates import AsyncTemplates, Templates
from .test_emails import AsyncTestEmails, TestEmails
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
    "Automations",
    "AsyncAutomations",
    "Billing",
    "AsyncBilling",
    "Campaigns",
    "AsyncCampaigns",
    "Contacts",
    "AsyncContacts",
    "DedicatedIps",
    "AsyncDedicatedIps",
    "Deliverability",
    "AsyncDeliverability",
    "Domains",
    "AsyncDomains",
    "Emails",
    "AsyncEmails",
    "Events",
    "AsyncEvents",
    "Inbound",
    "AsyncInbound",
    "NotificationPreferencesResource",
    "AsyncNotificationPreferencesResource",
    "Organizations",
    "AsyncOrganizations",
    "Regions",
    "AsyncRegions",
    "Status",
    "AsyncStatus",
    "Suppression",
    "AsyncSuppression",
    "Team",
    "AsyncTeam",
    "Templates",
    "AsyncTemplates",
    "TestEmails",
    "AsyncTestEmails",
    "Unsubscribes",
    "AsyncUnsubscribes",
    "Webhooks",
    "AsyncWebhooks",
    "verify_signature",
]
