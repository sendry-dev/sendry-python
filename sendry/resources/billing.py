"""
Billing resource — get_plan, get_usage, create_checkout, create_portal.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Union

from .._client import AsyncHttpClient, HttpClient
from .._types import (
    BillingPlan,
    BillingUsage,
    CheckoutSession,
    CreateCheckoutParams,
    CreatePortalParams,
    PortalSession,
)


def _map_checkout_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """Convert snake_case Python keys to camelCase for the billing API."""
    out = dict(params)
    if "billing_period" in out:
        out["billingPeriod"] = out.pop("billing_period")
    if "success_url" in out:
        out["successUrl"] = out.pop("success_url")
    if "cancel_url" in out:
        out["cancelUrl"] = out.pop("cancel_url")
    return out


def _map_portal_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """Convert snake_case Python keys to camelCase for the billing API."""
    out = dict(params)
    if "return_url" in out:
        out["returnUrl"] = out.pop("return_url")
    return out


class Billing:
    """
    Synchronous billing resource.

    Access via ``sendry.billing``.
    """

    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def get_plan(self) -> BillingPlan:
        """
        Get the current billing plan for your organisation.

        Returns:
            BillingPlan with ``plan``, ``has_subscription``, and ``billing_period``.

        Example::

            plan = sendry.billing.get_plan()
            print(f"Plan: {plan['plan']}, Period: {plan['billing_period']}")
        """
        return self._client.get("/v1/billing/plan")

    def get_usage(self) -> BillingUsage:
        """
        Get the current billing period email usage.

        Returns:
            BillingUsage with sent count, plan limit, and overage information.

        Example::

            usage = sendry.billing.get_usage()
            pct = usage["emails_sent_this_period"] / usage["plan_limit"] * 100
            print(f"Used {pct:.1f}% of monthly quota")
        """
        return self._client.get("/v1/billing/usage")

    def create_checkout(
        self, params: Union[CreateCheckoutParams, Dict[str, Any]]
    ) -> CheckoutSession:
        """
        Create a Stripe checkout session to upgrade or change your plan.

        Args:
            params: Must include ``plan`` (e.g. ``"pro"``).
                Optional: ``billing_period`` (``"monthly"`` or ``"annual"``),
                ``success_url``, ``cancel_url``.

        Returns:
            CheckoutSession with a ``url`` to redirect the user to.

        Example::

            session = sendry.billing.create_checkout({
                "plan": "pro",
                "billing_period": "annual",
                "success_url": "https://app.example.com/billing?success=1",
                "cancel_url": "https://app.example.com/billing",
            })
            # Redirect user to session["url"]
        """
        return self._client.post("/v1/billing/checkout", _map_checkout_params(dict(params)))

    def create_portal(
        self, params: Optional[Union[CreatePortalParams, Dict[str, Any]]] = None
    ) -> PortalSession:
        """
        Create a Stripe billing portal session for managing subscriptions.

        Args:
            params: Optional ``return_url`` to redirect back to after the portal.

        Returns:
            PortalSession with a ``url`` to redirect the user to.

        Example::

            portal = sendry.billing.create_portal({
                "return_url": "https://app.example.com/settings/billing",
            })
            # Redirect user to portal["url"]
        """
        body = _map_portal_params(dict(params)) if params else {}
        return self._client.post("/v1/billing/portal", body)


class AsyncBilling:
    """
    Asynchronous billing resource.

    Access via ``async_sendr.billing``.
    """

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def get_plan(self) -> BillingPlan:
        """Get current plan. See :meth:`Billing.get_plan`."""
        return await self._client.get("/v1/billing/plan")

    async def get_usage(self) -> BillingUsage:
        """Get billing usage. See :meth:`Billing.get_usage`."""
        return await self._client.get("/v1/billing/usage")

    async def create_checkout(
        self, params: Union[CreateCheckoutParams, Dict[str, Any]]
    ) -> CheckoutSession:
        """Create checkout session. See :meth:`Billing.create_checkout`."""
        return await self._client.post(
            "/v1/billing/checkout", _map_checkout_params(dict(params))
        )

    async def create_portal(
        self, params: Optional[Union[CreatePortalParams, Dict[str, Any]]] = None
    ) -> PortalSession:
        """Create portal session. See :meth:`Billing.create_portal`."""
        body = _map_portal_params(dict(params)) if params else {}
        return await self._client.post("/v1/billing/portal", body)


__all__ = ["Billing", "AsyncBilling"]
