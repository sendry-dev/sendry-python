"""
Type definitions for the Sendry Python SDK.

All types use TypedDict for full IDE support and runtime introspection.
API responses use snake_case matching the JSON field names returned by the API.
"""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, TypedDict, Union


# ---------------------------------------------------------------------------
# Shared
# ---------------------------------------------------------------------------


class PaginatedResponse(TypedDict):
    """Cursor-paginated list response wrapper."""

    data: List[Any]
    has_more: bool
    next_cursor: Optional[str]


class DeleteResponse(TypedDict):
    """Acknowledgement returned after a successful deletion."""

    deleted: bool


# ---------------------------------------------------------------------------
# Emails
# ---------------------------------------------------------------------------


class Tag(TypedDict):
    """An email tag used for filtering and analytics."""

    name: str
    value: str


class Attachment(TypedDict, total=False):
    """An email attachment."""

    filename: str
    """File name including extension (required)."""
    content: str
    """Base64-encoded file content (required)."""
    content_type: str
    """MIME type. Defaults to application/octet-stream."""


class SendEmailParams(TypedDict, total=False):
    """Parameters for sending a single email."""

    from_: str
    """Sender address — note: maps to the ``from`` JSON key."""
    to: Union[str, List[str]]
    cc: Union[str, List[str]]
    bcc: Union[str, List[str]]
    reply_to: str
    subject: str
    html: str
    text: str
    tags: List[Tag]
    headers: Dict[str, str]
    scheduled_at: str
    """ISO 8601 datetime to schedule the email."""
    template_id: str
    variables: Dict[str, Any]
    attachments: List[Attachment]
    tracking: bool


class SendEmailResponse(TypedDict):
    """Response returned after a successful email send."""

    id: str
    from_: str
    to: List[str]
    subject: str
    status: str
    created_at: str


class Email(TypedDict):
    """Full email object returned by get/list."""

    id: str
    from_: str
    to: List[str]
    subject: str
    status: str
    created_at: str
    sent_at: Optional[str]
    last_event: Optional[str]
    attachments: Optional[List[Dict[str, str]]]


class ListEmailsParams(TypedDict, total=False):
    """Query parameters for listing emails."""

    status: str
    limit: int
    cursor: str


class BatchEmailItem(TypedDict, total=False):
    """A single email item within a batch send request."""

    from_: str
    to: Union[str, List[str]]
    cc: Union[str, List[str]]
    bcc: Union[str, List[str]]
    reply_to: str
    subject: str
    html: str
    text: str
    tags: List[Tag]
    variables: Dict[str, Any]
    attachments: List[Attachment]


class SendBatchParams(TypedDict, total=False):
    """Parameters for sending a batch of emails."""

    from_: str
    subject: str
    template_id: str
    emails: List[BatchEmailItem]


class BatchEmailResponse(TypedDict):
    """Response returned after a successful batch send."""

    data: List[Dict[str, str]]


class SendMarketingEmailParams(TypedDict, total=False):
    """Parameters for sending a marketing email."""

    from_: str
    to: Union[str, List[str]]
    subject: str
    html: str
    text: str
    reply_to: str
    headers: Dict[str, str]
    tags: List[Tag]
    unsubscribe_url: str
    list_id: str
    scheduled_at: str
    template_id: str


class CancelEmailResponse(TypedDict):
    """Response returned after cancelling a queued email."""

    id: str
    status: Literal["cancelled"]


# ---------------------------------------------------------------------------
# Domains
# ---------------------------------------------------------------------------


class DnsRecord(TypedDict, total=False):
    """A single DNS record required to verify a domain."""

    type: str
    host: str
    value: str
    name: str
    priority: int
    verified: bool


class Domain(TypedDict):
    """A verified or pending domain."""

    id: str
    name: str
    status: str
    dns_records: List[DnsRecord]
    created_at: str


class CreateDomainParams(TypedDict):
    """Parameters for adding a domain."""

    name: str


class VerifyDomainResponse(TypedDict):
    """Result of a domain verification check."""

    id: str
    name: str
    status: str
    spf_verified: bool
    dkim_verified: bool
    dmarc_verified: bool


class ConfigureBimiParams(TypedDict, total=False):
    """Parameters for configuring BIMI on a domain."""

    logo_url: str
    """SVG logo URL (must be publicly accessible, required)."""
    vmc_url: str
    """Verified Mark Certificate URL (optional)."""
    selector: str
    """BIMI selector name. Defaults to 'default'."""


class BimiConfig(TypedDict):
    """BIMI configuration for a domain."""

    id: str
    domain_id: str
    logo_url: str
    vmc_url: Optional[str]
    selector: str
    status: str
    dns_record: Optional[str]
    verified_at: Optional[str]
    created_at: str
    updated_at: str


class VerifyBimiResponse(TypedDict):
    """Result of a BIMI verification check."""

    verified: bool
    status: str


# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------


class TemplateVariable(TypedDict, total=False):
    """Definition of a template variable."""

    type: str
    required: bool
    default: Any


class CreateTemplateParams(TypedDict, total=False):
    """Parameters for creating a template."""

    name: str
    subject: str
    html: str
    engine: Literal["html", "react"]
    variables: Dict[str, TemplateVariable]


class UpdateTemplateParams(TypedDict, total=False):
    """Parameters for updating a template."""

    name: str
    subject: str
    html: str
    engine: Literal["html", "react"]
    variables: Dict[str, TemplateVariable]


class Template(TypedDict):
    """A saved email template."""

    id: str
    name: str
    subject: Optional[str]
    html: Optional[str]
    engine: str
    variables: Optional[Dict[str, TemplateVariable]]
    created_at: str
    updated_at: str


class RenderTemplateParams(TypedDict, total=False):
    """Parameters for rendering a template."""

    variables: Dict[str, str]


class RenderTemplateResponse(TypedDict):
    """Rendered template output."""

    html: str
    text: str


# ---------------------------------------------------------------------------
# API Keys
# ---------------------------------------------------------------------------

ApiKeyScope = Literal["full_access", "sending_access", "read_only"]


class CreateApiKeyParams(TypedDict, total=False):
    """Parameters for creating an API key."""

    name: str
    scope: ApiKeyScope


class ApiKey(TypedDict):
    """An API key record (key value is masked)."""

    id: str
    name: str
    scope: str
    key_prefix: str
    last_used_at: Optional[str]
    created_at: str


class ApiKeyCreated(TypedDict):
    """Response returned when a new API key is created (key shown once)."""

    id: str
    name: str
    scope: str
    key: str
    created_at: str


# ---------------------------------------------------------------------------
# Webhooks
# ---------------------------------------------------------------------------


class CreateWebhookParams(TypedDict):
    """Parameters for creating a webhook."""

    url: str
    events: List[str]


class UpdateWebhookParams(TypedDict, total=False):
    """Parameters for updating a webhook."""

    url: str
    events: List[str]
    active: bool


class Webhook(TypedDict):
    """A webhook endpoint (includes signing secret)."""

    id: str
    url: str
    events: List[str]
    secret: str
    active: bool
    created_at: str
    updated_at: str


class WebhookListItem(TypedDict):
    """A webhook endpoint summary (no secret)."""

    id: str
    url: str
    events: List[str]
    active: bool
    created_at: str
    updated_at: str


# ---------------------------------------------------------------------------
# Analytics
# ---------------------------------------------------------------------------


class AnalyticsParams(TypedDict, total=False):
    """Parameters for analytics queries."""

    from_: str
    """Start date (ISO 8601, required)."""
    to: str
    """End date (ISO 8601, required)."""
    granularity: Literal["hour", "day", "week", "month"]
    tag: str
    domain: str


class AnalyticsBucket(TypedDict):
    """A single timeseries bucket in analytics results."""

    date: str
    sent: int
    delivered: int
    opened: int
    clicked: int
    bounced: int
    complained: int


class AnalyticsSummary(TypedDict):
    """Aggregate analytics summary statistics."""

    sent: int
    delivered: int
    opened: int
    clicked: int
    bounced: int
    complained: int
    delivery_rate: float
    open_rate: float
    click_rate: float
    bounce_rate: float
    complaint_rate: float


class AnalyticsResponse(TypedDict):
    """Full analytics response with summary and timeseries data."""

    summary: AnalyticsSummary
    timeseries: List[AnalyticsBucket]


class LogsParams(TypedDict, total=False):
    """Parameters for querying email event logs."""

    email_id: str
    type: str
    to: str
    from_date: str
    to_date: str
    limit: int
    cursor: str


class LogEvent(TypedDict):
    """A single email event log entry."""

    id: str
    email_id: str
    type: str
    recipient: str
    metadata: Optional[Any]
    created_at: str


class CohortParams(TypedDict, total=False):
    """Parameters for cohort analysis."""

    from_: str
    to: str
    granularity: Literal["day", "week", "month"]
    metric: Literal["open_rate", "click_rate", "delivery_rate"]


class CohortBucket(TypedDict):
    """A single cohort analysis bucket."""

    cohort_date: str
    period_offset: int
    total_sent: int
    metric_value: float


class CohortResponse(TypedDict):
    """Cohort analysis response."""

    cohorts: List[CohortBucket]
    granularity: str
    metric: str


class BenchmarkParams(TypedDict, total=False):
    """Parameters for benchmark comparison queries."""

    from_: str
    to: str
    granularity: Literal["day", "week", "month"]


class BenchmarkBucket(TypedDict):
    """Cross-org benchmark data for a single time period."""

    date: str
    your_delivery_rate: float
    your_open_rate: float
    your_click_rate: float
    avg_delivery_rate: float
    avg_open_rate: float
    avg_click_rate: float
    p50_delivery_rate: float
    p50_open_rate: float
    p50_click_rate: float
    p75_delivery_rate: float
    p75_open_rate: float
    p75_click_rate: float


class BenchmarkResponse(TypedDict):
    """Benchmark comparison response."""

    data: List[BenchmarkBucket]
    benchmark_opt_in: bool
    org_count: int


class BreakdownParams(TypedDict, total=False):
    """Parameters for analytics breakdowns."""

    from_: str
    to: str
    group_by: Literal["domain", "template"]
    limit: int


class BreakdownItem(TypedDict):
    """A single breakdown item (domain or template)."""

    id: Optional[str]
    name: Optional[str]
    sent: int
    delivered: int
    opened: int
    clicked: int
    bounced: int
    complained: int
    delivery_rate: float
    open_rate: float
    click_rate: float


class BreakdownResponse(TypedDict):
    """Analytics breakdown response."""

    data: List[BreakdownItem]
    group_by: str


class ComparisonPeriodStats(TypedDict):
    """Stats for one period in a period comparison."""

    sent: int
    delivered: int
    opened: int
    clicked: int
    bounced: int
    complained: int
    delivery_rate: float
    open_rate: float
    click_rate: float
    bounce_rate: float
    complaint_rate: float


class ComparisonResponse(TypedDict):
    """Period-over-period comparison response."""

    current: ComparisonPeriodStats
    previous: ComparisonPeriodStats
    changes: Dict[str, float]


class ExportParams(TypedDict, total=False):
    """Parameters for exporting analytics data."""

    from_: str
    to: str
    granularity: Literal["hour", "day", "week", "month"]
    format: Literal["csv", "json"]
    domain: str


# ---------------------------------------------------------------------------
# Suppression
# ---------------------------------------------------------------------------

SuppressionReason = Literal["hard_bounce", "complaint", "unsubscribe", "manual"]


class AddSuppressionParams(TypedDict, total=False):
    """Parameters for adding an address to the suppression list."""

    email: str
    reason: SuppressionReason


class SuppressionEntry(TypedDict):
    """A suppressed email address."""

    email: str
    reason: str
    created_at: str


# ---------------------------------------------------------------------------
# Unsubscribes
# ---------------------------------------------------------------------------


class CreateUnsubscribeParams(TypedDict, total=False):
    """Parameters for adding an unsubscribe record."""

    email: str
    list_id: str
    reason: str


class BatchUnsubscribeParams(TypedDict, total=False):
    """Parameters for batch-adding unsubscribe records."""

    emails: List[str]
    list_id: str
    reason: str


class BatchUnsubscribeResponse(TypedDict):
    """Result of a batch unsubscribe operation."""

    inserted: int


class UnsubscribeEntry(TypedDict):
    """A single unsubscribe record."""

    id: str
    email: str
    list_id: Optional[str]
    reason: Optional[str]
    created_at: str


class ListUnsubscribesParams(TypedDict, total=False):
    """Parameters for listing unsubscribe records."""

    email: str
    list_id: str
    limit: int
    cursor: str


# ---------------------------------------------------------------------------
# Contacts
# ---------------------------------------------------------------------------


class CreateContactParams(TypedDict, total=False):
    """Parameters for creating a contact."""

    email: str
    first_name: str
    last_name: str
    metadata: Dict[str, Any]
    unsubscribed: bool
    audience_id: str


class UpdateContactParams(TypedDict, total=False):
    """Parameters for updating a contact."""

    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    metadata: Optional[Dict[str, Any]]
    unsubscribed: bool


class Contact(TypedDict):
    """A contact record."""

    id: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    metadata: Optional[Any]
    unsubscribed: bool
    created_at: str
    updated_at: str


class ListContactsParams(TypedDict, total=False):
    """Parameters for listing contacts."""

    email: str
    audience_id: str
    limit: int
    cursor: str


class BulkImportContactItem(TypedDict, total=False):
    """A single contact item in a bulk import."""

    email: str
    first_name: str
    last_name: str
    metadata: Dict[str, Any]
    unsubscribed: bool


class BulkImportContactsParams(TypedDict, total=False):
    """Parameters for bulk importing contacts."""

    contacts: List[BulkImportContactItem]
    audience_id: str


class BulkImportResult(TypedDict):
    """Result of a bulk contact import."""

    created: int
    updated: int
    total: int


# ---------------------------------------------------------------------------
# Audiences
# ---------------------------------------------------------------------------


class CreateAudienceParams(TypedDict, total=False):
    """Parameters for creating an audience."""

    name: str
    description: str


class UpdateAudienceParams(TypedDict, total=False):
    """Parameters for updating an audience."""

    name: str
    description: Optional[str]


class Audience(TypedDict):
    """An audience (contact list)."""

    id: str
    name: str
    description: Optional[str]
    member_count: int
    created_at: str
    updated_at: str


class AddContactsToAudienceParams(TypedDict):
    """Parameters for adding contacts to an audience."""

    contact_ids: List[str]


class AddContactsToAudienceResult(TypedDict):
    """Result of adding contacts to an audience."""

    added: int


# ---------------------------------------------------------------------------
# Campaigns
# ---------------------------------------------------------------------------

CampaignStatus = Literal[
    "draft", "scheduled", "sending", "paused", "sent", "cancelled"
]


class CampaignStats(TypedDict):
    """Delivery and engagement statistics for a campaign."""

    total_recipients: int
    sent_count: int
    delivered_count: int
    opened_count: int
    clicked_count: int
    bounced_count: int
    complained_count: int
    unsubscribed_count: int
    failed_count: int


class Campaign(TypedDict):
    """A full campaign record including stats."""

    id: str
    name: str
    subject: str
    from_: str
    reply_to: Optional[str]
    preview_text: Optional[str]
    audience_id: str
    template_id: Optional[str]
    html: Optional[str]
    text: Optional[str]
    status: str
    scheduled_at: Optional[str]
    send_started_at: Optional[str]
    sent_at: Optional[str]
    stats: CampaignStats
    created_at: str
    updated_at: str


class CampaignListItem(TypedDict):
    """A campaign summary as returned in list responses."""

    id: str
    name: str
    subject: str
    from_: str
    audience_id: str
    status: str
    scheduled_at: Optional[str]
    sent_at: Optional[str]
    stats: CampaignStats
    created_at: str
    updated_at: str


class CreateCampaignParams(TypedDict, total=False):
    """Parameters for creating a campaign."""

    name: str
    subject: str
    from_: str
    reply_to: str
    preview_text: str
    audience_id: str
    template_id: str
    html: str
    text: str


class UpdateCampaignParams(TypedDict, total=False):
    """Parameters for updating a campaign."""

    name: str
    subject: str
    from_: str
    reply_to: Optional[str]
    preview_text: Optional[str]
    audience_id: str
    template_id: Optional[str]
    html: Optional[str]
    text: Optional[str]


class ScheduleCampaignParams(TypedDict):
    """Parameters for scheduling a campaign."""

    scheduled_at: str
    """ISO 8601 datetime when the campaign should be sent."""


class CampaignActionResponse(TypedDict):
    """Response returned after a campaign action (send, cancel, pause, etc.)."""

    id: str
    status: str


class ListCampaignsParams(TypedDict, total=False):
    """Parameters for listing campaigns."""

    status: str
    limit: int
    cursor: str


# ---------------------------------------------------------------------------
# Billing
# ---------------------------------------------------------------------------


class BillingPlan(TypedDict):
    """Current billing plan information."""

    plan: str
    has_subscription: bool
    billing_period: Literal["monthly", "annual"]


class BillingUsage(TypedDict):
    """Current billing period usage."""

    emails_sent_this_period: int
    plan_limit: int
    overage_count: int
    overage_rate: Optional[float]
    period_end: Optional[str]


class CreateCheckoutParams(TypedDict, total=False):
    """Parameters for creating a Stripe checkout session."""

    plan: str
    billing_period: Literal["monthly", "annual"]
    success_url: str
    cancel_url: str


class CreatePortalParams(TypedDict, total=False):
    """Parameters for creating a Stripe billing portal session."""

    return_url: str


class CheckoutSession(TypedDict):
    """A Stripe checkout session."""

    url: str


class PortalSession(TypedDict):
    """A Stripe billing portal session."""

    url: str


# ---------------------------------------------------------------------------
# Team
# ---------------------------------------------------------------------------


class TeamMember(TypedDict):
    """A team member record."""

    id: str
    org_id: str
    user_id: Optional[str]
    email: str
    name: Optional[str]
    role: str
    status: str
    invited_at: str
    joined_at: Optional[str]


class ListTeamResponse(TypedDict):
    """Response for listing team members including seat information."""

    data: List[TeamMember]
    seats: Dict[str, Any]
    plan: str


class InviteTeamMemberParams(TypedDict, total=False):
    """Parameters for inviting a team member."""

    email: str
    role: str


class UpdateTeamMemberRoleParams(TypedDict):
    """Parameters for updating a team member's role."""

    role: str


# ---------------------------------------------------------------------------
# Pagination helpers
# ---------------------------------------------------------------------------


class PaginationParams(TypedDict, total=False):
    """Generic cursor pagination parameters."""

    limit: int
    cursor: str


# ---------------------------------------------------------------------------
# Dedicated IPs
# ---------------------------------------------------------------------------


class ProvisionDedicatedIpParams(TypedDict, total=False):
    """Parameters for provisioning a dedicated IP."""

    provider: Literal["ses", "mailgun"]


class DedicatedIp(TypedDict):
    """A dedicated IP address record."""

    id: str
    ip_address: Optional[str]
    status: str
    provider: str
    warmup_progress: Optional[int]
    created_at: str


class AssignIpParams(TypedDict):
    """Parameters for assigning a dedicated IP to a domain."""

    domain_id: str


class IpAssignment(TypedDict):
    """A dedicated IP to domain assignment record."""

    id: str
    ip_id: str
    domain_id: str
    created_at: str


# ---------------------------------------------------------------------------
# Deliverability
# ---------------------------------------------------------------------------


class ReputationQuery(TypedDict, total=False):
    """Query for reputation overview."""

    domain_id: str
    days: int


class ReputationHistoryQuery(TypedDict, total=False):
    """Query for reputation history."""

    from_: str
    to: str


class ReputationSnapshot(TypedDict):
    """A reputation snapshot."""

    score: int
    rating: str


class ReputationResponse(TypedDict):
    """Reputation overview response."""

    current: ReputationSnapshot
    history: List[Dict[str, Any]]
    domains: List[Dict[str, Any]]


class BlocklistQuery(TypedDict, total=False):
    """Query for blocklist status."""

    target: str
    target_type: Literal["domain", "ip"]


class BlocklistCheckBody(TypedDict):
    """Body for running an on-demand blocklist check."""

    target: str
    target_type: Literal["domain", "ip"]


class BlocklistResponse(TypedDict):
    """Blocklist status response."""

    results: List[Dict[str, Any]]
    alerts: List[Dict[str, Any]]
    summary: Dict[str, Any]


class DeliverabilityReportQuery(TypedDict, total=False):
    """Query for a deliverability report."""

    domain_id: str
    days: int


class DeliverabilityReport(TypedDict):
    """Comprehensive deliverability report."""

    reputation: Dict[str, Any]
    metrics: Dict[str, Any]
    blocklist_status: Dict[str, Any]
    recommendations: List[Dict[str, Any]]


# ---------------------------------------------------------------------------
# Inbound
# ---------------------------------------------------------------------------


class InboundEmail(TypedDict):
    """An inbound email record."""

    id: str
    from_: str
    to: str
    subject: Optional[str]
    html: Optional[str]
    text: Optional[str]
    attachments: Optional[List[Dict[str, Any]]]
    received_at: str


class InboundConfig(TypedDict):
    """Inbound webhook forwarding configuration."""

    url: Optional[str]
    secret: Optional[str]


class UpdateInboundConfigParams(TypedDict, total=False):
    """Parameters for updating inbound webhook config."""

    url: Optional[str]
    secret: str


# ---------------------------------------------------------------------------
# Notification Preferences
# ---------------------------------------------------------------------------


class NotificationPreferences(TypedDict, total=False):
    """User notification preferences."""

    bounce_alerts: bool
    complaint_alerts: bool
    weekly_digest: bool
    daily_summary: bool
    reputation_alerts: bool
    blocklist_alerts: bool


class UpdateNotificationPreferencesParams(TypedDict, total=False):
    """Parameters for updating notification preferences."""

    bounce_alerts: bool
    complaint_alerts: bool
    weekly_digest: bool
    daily_summary: bool
    reputation_alerts: bool
    blocklist_alerts: bool


# ---------------------------------------------------------------------------
# Organizations
# ---------------------------------------------------------------------------


class Organization(TypedDict):
    """An organisation record."""

    id: str
    name: str
    plan: str
    created_at: str


class UpdateOrganizationParams(TypedDict):
    """Parameters for updating an organisation."""

    name: str


class BrandingSettings(TypedDict, total=False):
    """Organisation branding settings."""

    brand_color: str
    brand_logo: Optional[str]
    unsubscribe_copy: Optional[str]
    footer_copy: Optional[str]


class UpdateBrandingParams(TypedDict, total=False):
    """Parameters for updating branding settings."""

    brand_color: str
    brand_logo: Optional[str]
    unsubscribe_copy: Optional[str]
    footer_copy: Optional[str]


# ---------------------------------------------------------------------------
# Regions
# ---------------------------------------------------------------------------


class Region(TypedDict):
    """A SES region."""

    region_code: str
    display_name: str
    active: bool


DataResidency = Literal["none", "eu", "us", "ap"]


class OrgRegionSettings(TypedDict):
    """Org-level region settings."""

    default_region: str
    data_residency: str


class UpdateOrgRegionParams(TypedDict, total=False):
    """Parameters for updating org region settings."""

    default_region: str
    data_residency: DataResidency


class UpdateDomainRegionParams(TypedDict):
    """Parameters for setting a domain's region override."""

    region: Optional[str]


class RegionAnalyticsParams(TypedDict):
    """Parameters for region analytics."""

    from_: str
    to: str


class RegionAnalyticsResponse(TypedDict):
    """Region analytics response."""

    data: List[Dict[str, Any]]


# ---------------------------------------------------------------------------
# Status
# ---------------------------------------------------------------------------


class SystemStatus(TypedDict):
    """Current system status."""

    status: str
    components: List[Dict[str, Any]]
    incidents: List[Dict[str, Any]]
    sla_summary: Dict[str, Any]


class Incident(TypedDict):
    """A resolved or active incident."""

    id: str
    title: str
    status: str
    impact: Optional[str]
    started_at: str
    resolved_at: Optional[str]


class GetLatencyParams(TypedDict, total=False):
    """Parameters for fetching latency stats."""

    component: str
    hours: int


class LatencyStats(TypedDict):
    """Latency statistics for a component."""

    current_p50_ms: float
    target_p50_ms: float
    target_met: bool
    hourly: List[Dict[str, Any]]


# ---------------------------------------------------------------------------
# Test Emails
# ---------------------------------------------------------------------------


class TestEmailSummary(TypedDict):
    """A test email summary."""

    id: str
    subject: Optional[str]
    from_: str
    to: str
    message_type: Optional[str]
    created_at: str


class TestEmail(TypedDict):
    """A full test email record."""

    id: str
    subject: Optional[str]
    from_: str
    to: str
    html: Optional[str]
    text: Optional[str]
    message_type: Optional[str]
    headers: Optional[Dict[str, Any]]
    created_at: str


# ---------------------------------------------------------------------------
# Automations
# ---------------------------------------------------------------------------

AutomationStatus = Literal["draft", "active", "paused", "archived"]
AutomationTriggerType = Literal[
    "event", "contact_added_to_segment", "schedule", "manual"
]
AutomationStepType = Literal["send_email", "wait", "branch", "ab_split"]
AutomationReentryPolicy = Literal["once_per_contact", "cooldown", "always"]


class Automation(TypedDict):
    """An automation record."""

    id: str
    name: str
    description: Optional[str]
    status: str
    trigger_type: str
    trigger_config: Dict[str, Any]
    entry_segment_id: Optional[str]
    reentry_policy: str
    reentry_cooldown_seconds: Optional[int]
    total_runs: int
    active_runs: int
    completed_runs: int
    failed_runs: int
    created_at: str
    updated_at: str


class AutomationStep(TypedDict):
    """A single step in an automation."""

    id: str
    automation_id: str
    parent_step_id: Optional[str]
    branch_label: Optional[str]
    position: int
    type: str
    config: Dict[str, Any]
    created_at: str
    updated_at: str


class AutomationRun(TypedDict):
    """An automation run instance."""

    id: str
    automation_id: str
    contact_id: Optional[str]
    contact_email: str
    trigger_event_id: Optional[str]
    status: str
    current_step_id: Optional[str]
    context: Dict[str, Any]
    started_at: str
    completed_at: Optional[str]
    failed_at: Optional[str]
    failure_reason: Optional[str]
    created_at: str
    updated_at: str


class AutomationRunStep(TypedDict):
    """A single step execution within an automation run."""

    id: str
    run_id: str
    step_id: str
    status: str
    email_id: Optional[str]
    branch_taken: Optional[str]
    scheduled_for: Optional[str]
    started_at: Optional[str]
    completed_at: Optional[str]
    error: Optional[str]
    created_at: str


class CreateAutomationParams(TypedDict, total=False):
    """Parameters for creating an automation."""

    name: str
    description: str
    trigger_type: AutomationTriggerType
    trigger_config: Dict[str, Any]
    entry_segment_id: str
    reentry_policy: AutomationReentryPolicy
    reentry_cooldown_seconds: int


class UpdateAutomationParams(TypedDict, total=False):
    """Parameters for updating an automation."""

    name: str
    description: Optional[str]
    trigger_config: Dict[str, Any]
    entry_segment_id: Optional[str]
    reentry_policy: AutomationReentryPolicy
    reentry_cooldown_seconds: Optional[int]


class ListAutomationsParams(TypedDict, total=False):
    """Parameters for listing automations."""

    cursor: str
    status: AutomationStatus
    limit: int


class AddAutomationStepParams(TypedDict, total=False):
    """Parameters for adding an automation step."""

    parent_step_id: Optional[str]
    branch_label: Optional[str]
    position: int
    config: Dict[str, Any]


class UpdateAutomationStepParams(TypedDict, total=False):
    """Parameters for updating an automation step."""

    parent_step_id: Optional[str]
    branch_label: Optional[str]
    position: int
    config: Dict[str, Any]


class ListAutomationRunsParams(TypedDict, total=False):
    """Parameters for listing automation runs."""

    cursor: str
    status: str
    limit: int


class CreateAutomationRunParams(TypedDict, total=False):
    """Parameters for creating a manual automation run."""

    contact_id: str
    contact_email: str
    context: Dict[str, Any]


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------


class IngestEventParams(TypedDict, total=False):
    """Parameters for ingesting an event."""

    name: str
    event_id: str
    contact_email: str
    contact_id: str
    payload: Dict[str, Any]


class IngestedEvent(TypedDict):
    """An ingested event record."""

    id: str
    external_id: Optional[str]
    name: str
    contact_email: Optional[str]
    contact_id: Optional[str]
    payload: Dict[str, Any]
    received_at: str
    processed_at: Optional[str]
    triggered_runs: int


class ListEventsParams(TypedDict, total=False):
    """Parameters for listing ingested events."""

    cursor: str
    name: str
    limit: int


__all__ = [
    # Shared
    "PaginatedResponse",
    "DeleteResponse",
    "PaginationParams",
    # Emails
    "Tag",
    "Attachment",
    "SendEmailParams",
    "SendEmailResponse",
    "Email",
    "ListEmailsParams",
    "BatchEmailItem",
    "SendBatchParams",
    "BatchEmailResponse",
    "SendMarketingEmailParams",
    "CancelEmailResponse",
    # Domains
    "DnsRecord",
    "Domain",
    "CreateDomainParams",
    "VerifyDomainResponse",
    "ConfigureBimiParams",
    "BimiConfig",
    "VerifyBimiResponse",
    # Templates
    "TemplateVariable",
    "CreateTemplateParams",
    "UpdateTemplateParams",
    "Template",
    "RenderTemplateParams",
    "RenderTemplateResponse",
    # API Keys
    "ApiKeyScope",
    "CreateApiKeyParams",
    "ApiKey",
    "ApiKeyCreated",
    # Webhooks
    "CreateWebhookParams",
    "UpdateWebhookParams",
    "Webhook",
    "WebhookListItem",
    # Analytics
    "AnalyticsParams",
    "AnalyticsBucket",
    "AnalyticsSummary",
    "AnalyticsResponse",
    "LogsParams",
    "LogEvent",
    "CohortParams",
    "CohortBucket",
    "CohortResponse",
    "BenchmarkParams",
    "BenchmarkBucket",
    "BenchmarkResponse",
    "BreakdownParams",
    "BreakdownItem",
    "BreakdownResponse",
    "ComparisonPeriodStats",
    "ComparisonResponse",
    "ExportParams",
    # Suppression
    "SuppressionReason",
    "AddSuppressionParams",
    "SuppressionEntry",
    # Unsubscribes
    "CreateUnsubscribeParams",
    "BatchUnsubscribeParams",
    "BatchUnsubscribeResponse",
    "UnsubscribeEntry",
    "ListUnsubscribesParams",
    # Contacts
    "CreateContactParams",
    "UpdateContactParams",
    "Contact",
    "ListContactsParams",
    "BulkImportContactItem",
    "BulkImportContactsParams",
    "BulkImportResult",
    # Audiences
    "CreateAudienceParams",
    "UpdateAudienceParams",
    "Audience",
    "AddContactsToAudienceParams",
    "AddContactsToAudienceResult",
    # Campaigns
    "CampaignStatus",
    "CampaignStats",
    "Campaign",
    "CampaignListItem",
    "CreateCampaignParams",
    "UpdateCampaignParams",
    "ScheduleCampaignParams",
    "CampaignActionResponse",
    "ListCampaignsParams",
    # Billing
    "BillingPlan",
    "BillingUsage",
    "CreateCheckoutParams",
    "CreatePortalParams",
    "CheckoutSession",
    "PortalSession",
    # Team
    "TeamMember",
    "ListTeamResponse",
    "InviteTeamMemberParams",
    "UpdateTeamMemberRoleParams",
    # Dedicated IPs
    "ProvisionDedicatedIpParams",
    "DedicatedIp",
    "AssignIpParams",
    "IpAssignment",
    # Deliverability
    "ReputationQuery",
    "ReputationHistoryQuery",
    "ReputationSnapshot",
    "ReputationResponse",
    "BlocklistQuery",
    "BlocklistCheckBody",
    "BlocklistResponse",
    "DeliverabilityReportQuery",
    "DeliverabilityReport",
    # Inbound
    "InboundEmail",
    "InboundConfig",
    "UpdateInboundConfigParams",
    # Notification Preferences
    "NotificationPreferences",
    "UpdateNotificationPreferencesParams",
    # Organizations
    "Organization",
    "UpdateOrganizationParams",
    "BrandingSettings",
    "UpdateBrandingParams",
    # Regions
    "Region",
    "DataResidency",
    "OrgRegionSettings",
    "UpdateOrgRegionParams",
    "UpdateDomainRegionParams",
    "RegionAnalyticsParams",
    "RegionAnalyticsResponse",
    # Status
    "SystemStatus",
    "Incident",
    "GetLatencyParams",
    "LatencyStats",
    # Test Emails
    "TestEmailSummary",
    "TestEmail",
    # Automations
    "AutomationStatus",
    "AutomationTriggerType",
    "AutomationStepType",
    "AutomationReentryPolicy",
    "Automation",
    "AutomationStep",
    "AutomationRun",
    "AutomationRunStep",
    "CreateAutomationParams",
    "UpdateAutomationParams",
    "ListAutomationsParams",
    "AddAutomationStepParams",
    "UpdateAutomationStepParams",
    "ListAutomationRunsParams",
    "CreateAutomationRunParams",
    # Events
    "IngestEventParams",
    "IngestedEvent",
    "ListEventsParams",
]
