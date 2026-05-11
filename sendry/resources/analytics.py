"""
Analytics resource — stats, logs, cohorts, benchmarks, breakdowns, comparison, export.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Union

from .._client import AsyncHttpClient, HttpClient
from .._types import (
    AnalyticsParams,
    AnalyticsResponse,
    BenchmarkParams,
    BenchmarkResponse,
    BreakdownParams,
    BreakdownResponse,
    CohortParams,
    CohortResponse,
    ComparisonResponse,
    ExportParams,
    LogsParams,
    PaginatedResponse,
)


def _map_analytics_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """Map ``from_`` key to ``from`` for analytics query parameters."""
    out = dict(params)
    if "from_" in out:
        out["from"] = out.pop("from_")
    return out


class Analytics:
    """
    Synchronous analytics resource.

    Access via ``sendry.analytics``.
    """

    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def stats(self, params: Union[AnalyticsParams, Dict[str, Any]]) -> AnalyticsResponse:
        """
        Get aggregated email analytics with a summary and timeseries data.

        Args:
            params: Must include ``from_`` and ``to`` (ISO 8601 dates).
                Optional: ``granularity`` (``"hour"``, ``"day"``, ``"week"``, ``"month"``),
                ``tag``, ``domain``.

        Returns:
            AnalyticsResponse with ``summary`` rates and ``timeseries`` buckets.

        Example::

            data = sendry.analytics.stats({
                "from_": "2025-01-01",
                "to": "2025-01-31",
                "granularity": "day",
            })
            print(f"Delivery rate: {data['summary']['delivery_rate']:.1%}")
        """
        return self._client.get("/v1/analytics", _map_analytics_params(dict(params)))

    def logs(
        self, params: Optional[Union[LogsParams, Dict[str, Any]]] = None
    ) -> PaginatedResponse:
        """
        Get email event logs with optional filtering and pagination.

        Args:
            params: Optional filters — ``email_id``, ``type``, ``to``,
                ``from_date``, ``to_date``, ``cursor``, ``limit``.

        Returns:
            PaginatedResponse of LogEvent objects.

        Example::

            logs = sendry.analytics.logs({
                "email_id": "em_abc123",
                "type": "delivered",
            })
            for event in logs["data"]:
                print(event["type"], event["created_at"])
        """
        mapped = _map_analytics_params(dict(params)) if params else None
        return self._client.get("/v1/logs", mapped)

    def cohorts(self, params: Union[CohortParams, Dict[str, Any]]) -> CohortResponse:
        """
        Get cohort analysis — engagement rates over time since the send date.

        Args:
            params: Must include ``from_`` and ``to``. Optional: ``granularity``,
                ``metric`` (``"open_rate"``, ``"click_rate"``, ``"delivery_rate"``).

        Returns:
            CohortResponse with cohort buckets and period offsets.

        Example::

            result = sendry.analytics.cohorts({
                "from_": "2025-01-01",
                "to": "2025-01-31",
                "metric": "open_rate",
            })
        """
        return self._client.get("/v1/analytics/cohorts", _map_analytics_params(dict(params)))

    def benchmarks(self, params: Union[BenchmarkParams, Dict[str, Any]]) -> BenchmarkResponse:
        """
        Get cross-organisation benchmark comparisons.

        Your delivery, open, and click rates are compared against p50/p75/average
        from opted-in organisations.

        Args:
            params: Must include ``from_`` and ``to``. Optional: ``granularity``.

        Returns:
            BenchmarkResponse with per-bucket your vs industry metrics.

        Example::

            benchmarks = sendry.analytics.benchmarks({
                "from_": "2025-01-01",
                "to": "2025-01-31",
            })
        """
        return self._client.get("/v1/analytics/benchmarks", _map_analytics_params(dict(params)))

    def toggle_benchmark_opt_in(self, opt_in: bool) -> Any:
        """
        Opt in or out of anonymous benchmark data sharing.

        Args:
            opt_in: ``True`` to opt in, ``False`` to opt out.

        Returns:
            API acknowledgement response.
        """
        return self._client.post("/v1/analytics/benchmarks/opt-in", {"opt_in": opt_in})

    def breakdowns(self, params: Union[BreakdownParams, Dict[str, Any]]) -> BreakdownResponse:
        """
        Get analytics broken down by domain or template.

        Args:
            params: Must include ``from_``, ``to``, and ``group_by``
                (``"domain"`` or ``"template"``). Optional: ``limit``.

        Returns:
            BreakdownResponse with per-dimension delivery and engagement metrics.

        Example::

            data = sendry.analytics.breakdowns({
                "from_": "2025-01-01",
                "to": "2025-01-31",
                "group_by": "domain",
            })
            for item in data["data"]:
                print(item["name"], item["delivery_rate"])
        """
        return self._client.get("/v1/analytics/breakdowns", _map_analytics_params(dict(params)))

    def comparison(self, params: Union[AnalyticsParams, Dict[str, Any]]) -> ComparisonResponse:
        """
        Compare current period metrics against the equivalent previous period.

        Args:
            params: Date range parameters with ``from_`` and ``to``.

        Returns:
            ComparisonResponse with ``current``, ``previous``, and ``changes`` dicts.

        Example::

            result = sendry.analytics.comparison({
                "from_": "2025-02-01",
                "to": "2025-02-28",
            })
            delta = result["changes"]["open_rate_delta"]
            print(f"Open rate {'up' if delta > 0 else 'down'} {abs(delta):.1%}")
        """
        return self._client.get("/v1/analytics/comparison", _map_analytics_params(dict(params)))

    def export(self, params: Union[ExportParams, Dict[str, Any]]) -> Any:
        """
        Export analytics data as CSV or JSON.

        Args:
            params: Must include ``from_`` and ``to``. Optional: ``granularity``,
                ``format`` (``"csv"`` or ``"json"``), ``domain``.

        Returns:
            CSV string or parsed JSON dict depending on ``format``.

        Example::

            csv_data = sendry.analytics.export({
                "from_": "2025-01-01",
                "to": "2025-01-31",
                "format": "csv",
            })
        """
        return self._client.get("/v1/analytics/export", _map_analytics_params(dict(params)))


class AsyncAnalytics:
    """
    Asynchronous analytics resource.

    Access via ``async_sendr.analytics``.
    """

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def stats(self, params: Union[AnalyticsParams, Dict[str, Any]]) -> AnalyticsResponse:
        """Get analytics stats. See :meth:`Analytics.stats`."""
        return await self._client.get("/v1/analytics", _map_analytics_params(dict(params)))

    async def logs(
        self, params: Optional[Union[LogsParams, Dict[str, Any]]] = None
    ) -> PaginatedResponse:
        """Get event logs. See :meth:`Analytics.logs`."""
        mapped = _map_analytics_params(dict(params)) if params else None
        return await self._client.get("/v1/logs", mapped)

    async def cohorts(self, params: Union[CohortParams, Dict[str, Any]]) -> CohortResponse:
        """Get cohort analysis. See :meth:`Analytics.cohorts`."""
        return await self._client.get("/v1/analytics/cohorts", _map_analytics_params(dict(params)))

    async def benchmarks(
        self, params: Union[BenchmarkParams, Dict[str, Any]]
    ) -> BenchmarkResponse:
        """Get benchmark data. See :meth:`Analytics.benchmarks`."""
        return await self._client.get(
            "/v1/analytics/benchmarks", _map_analytics_params(dict(params))
        )

    async def toggle_benchmark_opt_in(self, opt_in: bool) -> Any:
        """Toggle benchmark opt-in. See :meth:`Analytics.toggle_benchmark_opt_in`."""
        return await self._client.post("/v1/analytics/benchmarks/opt-in", {"opt_in": opt_in})

    async def breakdowns(
        self, params: Union[BreakdownParams, Dict[str, Any]]
    ) -> BreakdownResponse:
        """Get analytics breakdowns. See :meth:`Analytics.breakdowns`."""
        return await self._client.get(
            "/v1/analytics/breakdowns", _map_analytics_params(dict(params))
        )

    async def comparison(
        self, params: Union[AnalyticsParams, Dict[str, Any]]
    ) -> ComparisonResponse:
        """Compare period analytics. See :meth:`Analytics.comparison`."""
        return await self._client.get(
            "/v1/analytics/comparison", _map_analytics_params(dict(params))
        )

    async def export(self, params: Union[ExportParams, Dict[str, Any]]) -> Any:
        """Export analytics data. See :meth:`Analytics.export`."""
        return await self._client.get(
            "/v1/analytics/export", _map_analytics_params(dict(params))
        )


__all__ = ["Analytics", "AsyncAnalytics"]
