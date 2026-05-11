"""
Webhook utility functions for the Sendry Python SDK.
"""

from __future__ import annotations

import hashlib
import hmac


def verify_signature(payload: str, signature: str, secret: str) -> bool:
    """
    Verify that a Sendry webhook payload was signed with the given secret.

    Sendry signs webhook payloads using HMAC-SHA256. The signature header has
    the format: ``t=<timestamp>,v1=<hex_signature>``

    The signed string is constructed as: ``{timestamp}.{raw_payload_body}``

    Args:
        payload: The raw request body string (before JSON parsing).
        signature: The value of the ``Sendry-Signature`` header.
        secret: Your webhook endpoint's signing secret (from the Sendry dashboard
            or the ``secret`` field returned when creating a webhook).

    Returns:
        ``True`` if the signature is valid, ``False`` otherwise.

    Raises:
        ValueError: If the signature header format is invalid.

    Example::

        # In a Flask route handler:
        is_valid = verify_signature(
            payload=request.get_data(as_text=True),
            signature=request.headers.get("Sendry-Signature", ""),
            secret=webhook_secret,
        )
        if not is_valid:
            abort(400, "Invalid webhook signature")

    Example with FastAPI::

        @app.post("/webhooks/sendry")
        async def handle_webhook(
            request: Request,
            x_sendr_signature: str = Header(alias="Sendry-Signature"),
        ):
            body = await request.body()
            if not verify_signature(body.decode(), x_sendr_signature, WEBHOOK_SECRET):
                raise HTTPException(status_code=400, detail="Invalid signature")
            data = await request.json()
            # process data...
    """
    if not signature:
        return False

    try:
        parts = dict(p.split("=", 1) for p in signature.split(",") if "=" in p)
    except Exception:
        return False

    timestamp = parts.get("t", "")
    v1 = parts.get("v1", "")

    if not timestamp or not v1:
        return False

    signed = f"{timestamp}.{payload}"
    expected = hmac.new(
        secret.encode("utf-8"),
        signed.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(expected, v1)


__all__ = ["verify_signature"]
