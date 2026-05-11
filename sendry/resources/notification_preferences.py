"""
Notification preferences resource — get and update user notification settings.
"""

from __future__ import annotations

from typing import Any, Dict, Union

from .._client import AsyncHttpClient, HttpClient
from .._types import NotificationPreferences, UpdateNotificationPreferencesParams


class NotificationPreferencesResource:
    """
    Synchronous notification preferences resource.

    Access via ``sendry.notification_preferences``.
    """

    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def get(self) -> NotificationPreferences:
        """Get the current user's notification preferences."""
        return self._client.get("/v1/notification-preferences")

    def update(
        self, params: Union[UpdateNotificationPreferencesParams, Dict[str, Any]]
    ) -> NotificationPreferences:
        """Update notification preferences. Only provided fields are changed."""
        return self._client.put("/v1/notification-preferences", dict(params))


class AsyncNotificationPreferencesResource:
    """
    Asynchronous notification preferences resource.

    Access via ``async_sendr.notification_preferences``.
    """

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def get(self) -> NotificationPreferences:
        """Get notification preferences. See :meth:`NotificationPreferencesResource.get`."""
        return await self._client.get("/v1/notification-preferences")

    async def update(
        self, params: Union[UpdateNotificationPreferencesParams, Dict[str, Any]]
    ) -> NotificationPreferences:
        """Update notification preferences. See :meth:`NotificationPreferencesResource.update`."""
        return await self._client.put("/v1/notification-preferences", dict(params))


__all__ = [
    "NotificationPreferencesResource",
    "AsyncNotificationPreferencesResource",
]
