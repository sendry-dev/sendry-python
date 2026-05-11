# sendry-python

The official Python SDK for the [Sendry](https://sendry.online) email API — a powerful, developer-first email sending platform.

## Installation

```bash
pip install sendry
```

Requires Python 3.9+ and `httpx>=0.27`.

## Quick Start

### Send your first email (sync)

```python
from sendry import Sendry

sendry = Sendry("sn_live_your_api_key")

response = sendry.emails.send({
    "from_": "hello@yourdomain.com",
    "to": "user@example.com",
    "subject": "Hello from Sendry!",
    "html": "<h1>Welcome!</h1><p>Your email, delivered.</p>",
    "text": "Welcome! Your email, delivered.",
})

print(response["id"])  # em_abc123
```

### Send your first email (async)

```python
import asyncio
from sendry import AsyncSendry

async def main():
    sendry = AsyncSendry("sn_live_your_api_key")

    response = await sendry.emails.send({
        "from_": "hello@yourdomain.com",
        "to": "user@example.com",
        "subject": "Hello from Sendry!",
        "html": "<h1>Welcome!</h1>",
    })

    print(response["id"])

asyncio.run(main())
```

> **Note on `from_`**: Python reserves `from` as a keyword, so this SDK uses `from_` in all places where the API expects a `from` field. The SDK maps this automatically before sending the request.

---

## Client Configuration

```python
sendry = Sendry(
    api_key="sn_live_abc123",
    base_url="https://api.sendry.online",   # default
    timeout=30.0,                        # seconds, default 30
    retries=3,                           # retries on 5xx/network errors, default 3
    default_headers={"X-Custom": "val"}, # merged into every request
)
```

### Retry behaviour

The client automatically retries on:
- HTTP 5xx server errors
- Network errors (connection refused, DNS failure)
- Timeouts

Retries use exponential backoff with delays of 1s, 2s, 4s. On HTTP 429 responses the `Retry-After` header is respected.

---

## Emails

### Send a single email

```python
response = sendry.emails.send({
    "from_": "Acme <hello@acme.com>",
    "to": ["alice@example.com", "bob@example.com"],
    "cc": "manager@acme.com",
    "subject": "Your order shipped!",
    "html": "<p>Your order is on its way.</p>",
    "text": "Your order is on its way.",
    "reply_to": "support@acme.com",
    "tags": [{"name": "category", "value": "transactional"}],
    "tracking": True,
    "attachments": [
        {
            "filename": "invoice.pdf",
            "content": "<base64-encoded-content>",
            "content_type": "application/pdf",
        }
    ],
})
print(response["id"])
```

### Schedule an email

```python
response = sendry.emails.send({
    "from_": "hello@example.com",
    "to": "user@example.com",
    "subject": "Scheduled email",
    "html": "<p>Delivered at the right time.</p>",
    "scheduled_at": "2026-04-01T09:00:00Z",
})
```

### Get an email

```python
email = sendry.emails.get("em_abc123")
print(email["status"])  # "delivered"
```

### List emails

```python
page = sendry.emails.list({"limit": 25, "status": "delivered"})
for email in page["data"]:
    print(email["id"], email["status"])

if page["has_more"]:
    next_page = sendry.emails.list({
        "cursor": page["next_cursor"],
        "limit": 25,
    })
```

### Send a batch

```python
result = sendry.emails.send_batch({
    "from_": "hello@example.com",
    "emails": [
        {"to": "alice@example.com", "subject": "Hi Alice", "html": "<p>Hi!</p>"},
        {"to": "bob@example.com",   "subject": "Hi Bob",   "html": "<p>Hi!</p>"},
    ],
})
for item in result["data"]:
    print(item["id"], item["status"])
```

### Send a marketing email

```python
sendry.emails.send_marketing({
    "from_": "news@acme.com",
    "to": "subscriber@example.com",
    "subject": "March Newsletter",
    "html": "<p>Check out what's new!</p>",
    "unsubscribe_url": "https://acme.com/unsubscribe?token=abc123",
    "list_id": "newsletter",
})
```

### Cancel a queued email

```python
result = sendry.emails.cancel("em_abc123")
print(result["status"])  # "cancelled"
```

---

## Domains

### Add a domain

```python
domain = sendry.domains.create({"name": "mail.example.com"})
for record in domain["dns_records"]:
    print(f"{record['type']} {record['host']} -> {record['value']}")
```

### Verify a domain

```python
result = sendry.domains.verify("dom_abc123")
print(result["spf_verified"], result["dkim_verified"])
```

### Configure BIMI

```python
bimi = sendry.domains.configure_bimi("dom_abc123", {
    "logo_url": "https://example.com/logo.svg",
    "vmc_url": "https://example.com/certificate.pem",
})
print(bimi["dns_record"])
```

---

## Templates

### Create and render a template

```python
template = sendry.templates.create({
    "name": "Welcome Email",
    "subject": "Welcome, {{name}}!",
    "html": "<h1>Hello {{name}}</h1><p>Thanks for signing up.</p>",
    "variables": {
        "name": {"type": "string", "required": True},
    },
})

rendered = sendry.templates.render(template["id"], {
    "variables": {"name": "Alice"},
})
print(rendered["html"])
```

### Use a template in an email

```python
sendry.emails.send({
    "from_": "hello@example.com",
    "to": "alice@example.com",
    "subject": "Welcome!",
    "template_id": template["id"],
    "variables": {"name": "Alice"},
})
```

---

## Contacts & Audiences

### Create a contact

```python
contact = sendry.contacts.create({
    "email": "jane@example.com",
    "first_name": "Jane",
    "last_name": "Doe",
    "metadata": {"plan": "pro", "signup_source": "web"},
})
```

### Bulk import contacts

```python
result = sendry.contacts.import_contacts({
    "contacts": [
        {"email": "alice@example.com", "first_name": "Alice"},
        {"email": "bob@example.com",   "first_name": "Bob"},
    ],
    "audience_id": "aud_abc123",
})
print(f"Created: {result['created']}, Updated: {result['updated']}")
```

### Create an audience and add contacts

```python
audience = sendry.audiences.create({
    "name": "Newsletter Subscribers",
    "description": "Weekly newsletter recipients",
})

sendry.audiences.add_contacts(audience["id"], {
    "contact_ids": [contact["id"]],
})
```

---

## Campaigns

### Create and send a campaign

```python
campaign = sendry.campaigns.create({
    "name": "March Newsletter",
    "subject": "What's new in March",
    "from_": "Acme <hello@acme.com>",
    "audience_id": "aud_abc123",
    "html": "<h1>March Updates</h1><p>Here's what's new...</p>",
})

# Schedule for later
sendry.campaigns.schedule(campaign["id"], {
    "scheduled_at": "2026-03-15T10:00:00Z",
})

# Or send immediately
sendry.campaigns.send(campaign["id"])
```

### Check campaign stats

```python
campaign = sendry.campaigns.get("cp_abc123")
stats = campaign["stats"]
print(f"Delivered: {stats['delivered_count']}/{stats['total_recipients']}")
print(f"Opened: {stats['opened_count']}")
```

---

## Analytics

### Get stats

```python
data = sendry.analytics.stats({
    "from_": "2025-01-01",
    "to": "2025-01-31",
    "granularity": "day",
})
summary = data["summary"]
print(f"Delivery rate: {summary['delivery_rate']:.1%}")
print(f"Open rate:     {summary['open_rate']:.1%}")
```

### Query event logs

```python
logs = sendry.analytics.logs({
    "email_id": "em_abc123",
    "type": "opened",
    "limit": 10,
})
for event in logs["data"]:
    print(event["recipient"], event["created_at"])
```

### Get cohort analysis

```python
cohorts = sendry.analytics.cohorts({
    "from_": "2025-01-01",
    "to": "2025-01-31",
    "metric": "open_rate",
    "granularity": "week",
})
```

### Compare periods

```python
comparison = sendry.analytics.comparison({
    "from_": "2025-02-01",
    "to": "2025-02-28",
})
delta = comparison["changes"]["open_rate_delta"]
print(f"Open rate {'improved' if delta > 0 else 'declined'} by {abs(delta):.1%}")
```

### Export data

```python
csv_data = sendry.analytics.export({
    "from_": "2025-01-01",
    "to": "2025-01-31",
    "format": "csv",
})
with open("analytics.csv", "w") as f:
    f.write(csv_data)
```

---

## Webhooks

### Create a webhook

```python
webhook = sendry.webhooks.create({
    "url": "https://example.com/webhooks/sendry",
    "events": [
        "email.delivered",
        "email.bounced",
        "email.opened",
        "email.clicked",
        "email.complained",
    ],
})
# Store the secret securely — needed to verify incoming payloads
webhook_secret = webhook["secret"]
```

### Verify webhook signatures

Use `verify_signature` in your webhook handler to confirm that incoming requests
genuinely originate from Sendry:

```python
from sendry import verify_signature

# Flask example
from flask import Flask, request, abort

app = Flask(__name__)
WEBHOOK_SECRET = "your_webhook_secret"

@app.post("/webhooks/sendry")
def handle_webhook():
    payload = request.get_data(as_text=True)
    signature = request.headers.get("X-Sendry-Signature", "")

    if not verify_signature(payload, signature, WEBHOOK_SECRET):
        abort(400, "Invalid webhook signature")

    data = request.get_json()
    event_type = data.get("type")

    if event_type == "email.delivered":
        print(f"Email delivered: {data['data']['email_id']}")
    elif event_type == "email.bounced":
        print(f"Email bounced: {data['data']['email_id']}")

    return "", 200
```

```python
# FastAPI example
from fastapi import FastAPI, Header, HTTPException, Request
from sendry import verify_signature

app = FastAPI()
WEBHOOK_SECRET = "your_webhook_secret"

@app.post("/webhooks/sendry")
async def handle_webhook(
    request: Request,
    sendry_signature: str = Header(alias="X-Sendry-Signature"),
):
    body = await request.body()
    if not verify_signature(body.decode(), sendry_signature, WEBHOOK_SECRET):
        raise HTTPException(status_code=400, detail="Invalid signature")

    data = await request.json()
    print(f"Received event: {data['type']}")
    return {"ok": True}
```

---

## Suppression & Unsubscribes

```python
# Add to suppression list
sendry.suppression.add({
    "email": "bounced@example.com",
    "reason": "hard_bounce",
})

# List suppressed addresses
page = sendry.suppression.list()

# Remove from suppression
sendry.suppression.remove("bounced@example.com")

# Add unsubscribe
sendry.unsubscribes.create({
    "email": "user@example.com",
    "list_id": "newsletter",
    "reason": "User requested removal",
})

# Batch unsubscribe
result = sendry.unsubscribes.create_batch({
    "emails": ["a@example.com", "b@example.com"],
    "list_id": "newsletter",
})
print(f"Inserted: {result['inserted']}")
```

---

## API Keys

```python
# Create a scoped API key
result = sendry.api_keys.create({
    "name": "CI/CD Pipeline Key",
    "scope": "sending_access",
})
# The key is only shown once — store it immediately
print(result["key"])

# List existing keys (values are masked)
keys = sendry.api_keys.list()
for key in keys["data"]:
    print(key["name"], key["key_prefix"], key["scope"])

# Revoke a key
sendry.api_keys.remove("ak_abc123")
```

Available scopes: `"full_access"`, `"sending_access"`, `"read_only"`

---

## Billing

```python
# Get current plan
plan = sendry.billing.get_plan()
print(f"Plan: {plan['plan']}, Period: {plan['billing_period']}")

# Get usage for current billing period
usage = sendry.billing.get_usage()
pct = usage["emails_sent_this_period"] / usage["plan_limit"] * 100
print(f"Used {pct:.1f}% of monthly quota ({usage['emails_sent_this_period']}/{usage['plan_limit']})")

# Upgrade plan — creates a Stripe checkout session
session = sendry.billing.create_checkout({
    "plan": "pro",
    "billing_period": "annual",
    "success_url": "https://app.example.com/billing?upgraded=1",
    "cancel_url": "https://app.example.com/billing",
})
print(f"Redirect to: {session['url']}")

# Open billing portal
portal = sendry.billing.create_portal({
    "return_url": "https://app.example.com/settings",
})
print(f"Portal URL: {portal['url']}")
```

---

## Team Management

```python
# List team members
team = sendry.team.list()
print(f"Team: {team['seats']['used']}/{team['seats']['limit']} seats used")
for member in team["data"]:
    print(f"  {member['email']} ({member['role']}) — {member['status']}")

# Invite a new member
invited = sendry.team.invite({
    "email": "alice@example.com",
    "role": "admin",
})

# Change a member's role
sendry.team.update_role("tm_abc123", {"role": "member"})

# Remove a member
sendry.team.remove("tm_abc123")
```

---

## Async Usage

Every resource has an `Async` variant accessible via `AsyncSendry`. All methods
are coroutines and must be awaited:

```python
import asyncio
from sendry import AsyncSendry

async def main():
    sendry = AsyncSendry("sn_live_abc123")

    # Send in parallel
    results = await asyncio.gather(
        sendry.emails.send({
            "from_": "hello@example.com",
            "to": "alice@example.com",
            "subject": "Hello Alice",
            "html": "<p>Hi!</p>",
        }),
        sendry.emails.send({
            "from_": "hello@example.com",
            "to": "bob@example.com",
            "subject": "Hello Bob",
            "html": "<p>Hi!</p>",
        }),
    )

    for r in results:
        print(r["id"])

    # Campaigns
    campaign = await sendry.campaigns.create({
        "name": "Welcome Series",
        "subject": "Welcome!",
        "from_": "hello@example.com",
        "audience_id": "aud_abc123",
        "html": "<p>Welcome!</p>",
    })
    await sendry.campaigns.send(campaign["id"])

asyncio.run(main())
```

---

## Error Handling

All SDK errors inherit from `SendryError`. Catch specific subclasses for
fine-grained handling:

```python
from sendry import (
    Sendry,
    ApiError,
    AuthenticationError,
    ValidationError,
    RateLimitError,
    NotFoundError,
    NetworkError,
)
import time

sendry = Sendry("sn_live_abc123")

try:
    email = sendry.emails.get("em_does_not_exist")
except AuthenticationError:
    print("Invalid API key — check your credentials")
except NotFoundError:
    print("Email not found")
except ValidationError as e:
    print(f"Validation failed: {e.message}")
    print(f"Details: {e.details}")
except RateLimitError as e:
    wait = e.retry_after or 60
    print(f"Rate limited. Retry after {wait}s")
    time.sleep(wait)
except ApiError as e:
    print(f"API error {e.status_code}: [{e.code}] {e.message}")
except NetworkError as e:
    print(f"Network error: {e.message}")
    if e.cause:
        print(f"Caused by: {e.cause}")
```

### Exception hierarchy

```
SendryError
├── ApiError               # 4xx/5xx HTTP responses
│   ├── AuthenticationError  # 401
│   ├── NotFoundError        # 404
│   ├── ValidationError      # 422 (has .details with field errors)
│   └── RateLimitError       # 429 (has .retry_after in seconds)
└── NetworkError             # connection/timeout failures (has .cause)
```

---

## License

MIT
