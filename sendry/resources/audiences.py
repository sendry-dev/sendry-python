"""
Audiences resource — create, list, get, update, remove, add_contacts, list_contacts, remove_contact.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Union
from urllib.parse import quote

from .._client import AsyncHttpClient, HttpClient
from .._types import (
    AddContactsToAudienceParams,
    AddContactsToAudienceResult,
    Audience,
    Contact,
    CreateAudienceParams,
    DeleteResponse,
    PaginatedResponse,
    PaginationParams,
    UpdateAudienceParams,
)


class Audiences:
    """
    Synchronous audiences resource.

    Access via ``sendry.audiences``.
    """

    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def create(self, params: Union[CreateAudienceParams, Dict[str, Any]]) -> Audience:
        """
        Create a new audience (contact list).

        Args:
            params: Must include ``name``. Optional ``description``.

        Returns:
            The created Audience object.

        Example::

            audience = sendry.audiences.create({
                "name": "Newsletter Subscribers",
                "description": "Weekly newsletter recipients",
            })
            print(audience["id"])
        """
        return self._client.post("/v1/audiences", dict(params))

    def list(self, params: Optional[Union[PaginationParams, Dict[str, Any]]] = None) -> PaginatedResponse:
        """
        List all audiences with member counts.

        Args:
            params: Optional ``limit`` and ``cursor`` for pagination.

        Returns:
            PaginatedResponse of Audience objects.
        """
        return self._client.get("/v1/audiences", dict(params) if params else None)

    def get(self, audience_id: str) -> Audience:
        """
        Get an audience by ID.

        Args:
            audience_id: The audience ID (e.g. ``aud_abc123``).

        Returns:
            Audience object including current ``member_count``.
        """
        return self._client.get(f"/v1/audiences/{quote(audience_id, safe='')}")

    def update(
        self, audience_id: str, params: Union[UpdateAudienceParams, Dict[str, Any]]
    ) -> Audience:
        """
        Update an audience's name or description.

        Args:
            audience_id: The audience ID.
            params: Fields to update. Use ``None`` for ``description`` to clear it.

        Returns:
            Updated Audience object.

        Example::

            updated = sendry.audiences.update("aud_abc123", {"name": "VIP Subscribers"})
        """
        return self._client.put(f"/v1/audiences/{quote(audience_id, safe='')}", dict(params))

    def remove(self, audience_id: str) -> DeleteResponse:
        """
        Delete an audience.

        Removes all contact memberships. Contacts themselves are not deleted.

        Args:
            audience_id: The audience ID.

        Returns:
            DeleteResponse acknowledging the deletion.
        """
        return self._client.delete(f"/v1/audiences/{quote(audience_id, safe='')}")

    def add_contacts(
        self, audience_id: str, params: Union[AddContactsToAudienceParams, Dict[str, Any]]
    ) -> AddContactsToAudienceResult:
        """
        Add one or more contacts to an audience by their IDs.

        Args:
            audience_id: The audience ID.
            params: Must include ``contact_ids`` list (max 100 per request).

        Returns:
            AddContactsToAudienceResult with ``added`` count.

        Example::

            result = sendry.audiences.add_contacts("aud_abc123", {
                "contact_ids": ["ct_1", "ct_2", "ct_3"],
            })
            print(f"Added {result['added']} contacts")
        """
        return self._client.post(
            f"/v1/audiences/{quote(audience_id, safe='')}/contacts", dict(params)
        )

    def list_contacts(
        self, audience_id: str, params: Optional[Union[PaginationParams, Dict[str, Any]]] = None
    ) -> PaginatedResponse:
        """
        List all contacts in an audience.

        Args:
            audience_id: The audience ID.
            params: Optional ``cursor`` and ``limit`` for pagination.

        Returns:
            PaginatedResponse of Contact objects.
        """
        return self._client.get(
            f"/v1/audiences/{quote(audience_id, safe='')}/contacts",
            dict(params) if params else None,
        )

    def remove_contact(self, audience_id: str, contact_id: str) -> DeleteResponse:
        """
        Remove a contact from an audience (does not delete the contact).

        Args:
            audience_id: The audience ID.
            contact_id: The contact ID to remove.

        Returns:
            DeleteResponse acknowledging the removal.

        Example::

            sendry.audiences.remove_contact("aud_abc123", "ct_xyz456")
        """
        return self._client.delete(
            f"/v1/audiences/{quote(audience_id, safe='')}/contacts/{quote(contact_id, safe='')}"
        )


class AsyncAudiences:
    """
    Asynchronous audiences resource.

    Access via ``async_sendr.audiences``.
    """

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def create(self, params: Union[CreateAudienceParams, Dict[str, Any]]) -> Audience:
        """Create an audience. See :meth:`Audiences.create`."""
        return await self._client.post("/v1/audiences", dict(params))

    async def list(
        self, params: Optional[Union[PaginationParams, Dict[str, Any]]] = None
    ) -> PaginatedResponse:
        """List audiences. See :meth:`Audiences.list`."""
        return await self._client.get("/v1/audiences", dict(params) if params else None)

    async def get(self, audience_id: str) -> Audience:
        """Get an audience. See :meth:`Audiences.get`."""
        return await self._client.get(f"/v1/audiences/{quote(audience_id, safe='')}")

    async def update(
        self, audience_id: str, params: Union[UpdateAudienceParams, Dict[str, Any]]
    ) -> Audience:
        """Update an audience. See :meth:`Audiences.update`."""
        return await self._client.put(
            f"/v1/audiences/{quote(audience_id, safe='')}", dict(params)
        )

    async def remove(self, audience_id: str) -> DeleteResponse:
        """Delete an audience. See :meth:`Audiences.remove`."""
        return await self._client.delete(f"/v1/audiences/{quote(audience_id, safe='')}")

    async def add_contacts(
        self, audience_id: str, params: Union[AddContactsToAudienceParams, Dict[str, Any]]
    ) -> AddContactsToAudienceResult:
        """Add contacts to an audience. See :meth:`Audiences.add_contacts`."""
        return await self._client.post(
            f"/v1/audiences/{quote(audience_id, safe='')}/contacts", dict(params)
        )

    async def list_contacts(
        self, audience_id: str, params: Optional[Union[PaginationParams, Dict[str, Any]]] = None
    ) -> PaginatedResponse:
        """List audience contacts. See :meth:`Audiences.list_contacts`."""
        return await self._client.get(
            f"/v1/audiences/{quote(audience_id, safe='')}/contacts",
            dict(params) if params else None,
        )

    async def remove_contact(self, audience_id: str, contact_id: str) -> DeleteResponse:
        """Remove a contact from an audience. See :meth:`Audiences.remove_contact`."""
        return await self._client.delete(
            f"/v1/audiences/{quote(audience_id, safe='')}/contacts/{quote(contact_id, safe='')}"
        )


__all__ = ["Audiences", "AsyncAudiences"]
