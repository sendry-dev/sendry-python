"""
Contacts resource — create, list, get, update, remove, import_contacts.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Union
from urllib.parse import quote

from .._client import AsyncHttpClient, HttpClient
from .._types import (
    BulkImportContactsParams,
    BulkImportResult,
    Contact,
    CreateContactParams,
    DeleteResponse,
    ListContactsParams,
    PaginatedResponse,
    UpdateContactParams,
)


class Contacts:
    """
    Synchronous contacts resource.

    Access via ``sendry.contacts``.
    """

    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def create(self, params: Union[CreateContactParams, Dict[str, Any]]) -> Contact:
        """
        Create a new contact.

        Args:
            params: Must include ``email``. Optional: ``first_name``,
                ``last_name``, ``metadata``, ``unsubscribed``, ``audience_id``.

        Returns:
            The created Contact object.

        Example::

            contact = sendry.contacts.create({
                "email": "jane@example.com",
                "first_name": "Jane",
                "last_name": "Doe",
            })
            print(contact["id"])
        """
        return self._client.post("/v1/contacts", dict(params))

    def list(
        self, params: Optional[Union[ListContactsParams, Dict[str, Any]]] = None
    ) -> PaginatedResponse:
        """
        List contacts with optional filtering.

        Args:
            params: Optional filters — ``email`` (partial match),
                ``audience_id``, ``cursor``, ``limit``.

        Returns:
            PaginatedResponse of Contact objects.

        Example::

            page = sendry.contacts.list({"audience_id": "aud_abc123", "limit": 50})
        """
        return self._client.get("/v1/contacts", dict(params) if params else None)

    def get(self, contact_id: str) -> Contact:
        """
        Get a contact by ID.

        Args:
            contact_id: The contact ID (e.g. ``ct_abc123``).

        Returns:
            Full Contact object.
        """
        return self._client.get(f"/v1/contacts/{quote(contact_id, safe='')}")

    def update(
        self, contact_id: str, params: Union[UpdateContactParams, Dict[str, Any]]
    ) -> Contact:
        """
        Update a contact.

        Args:
            contact_id: The contact ID.
            params: Fields to update. All are optional. Use ``None`` to clear
                nullable fields like ``first_name``, ``last_name``, ``metadata``.

        Returns:
            Updated Contact object.

        Example::

            updated = sendry.contacts.update("ct_abc123", {"unsubscribed": True})
        """
        return self._client.put(f"/v1/contacts/{quote(contact_id, safe='')}", dict(params))

    def remove(self, contact_id: str) -> DeleteResponse:
        """
        Delete a contact.

        Args:
            contact_id: The contact ID.

        Returns:
            DeleteResponse acknowledging the deletion.
        """
        return self._client.delete(f"/v1/contacts/{quote(contact_id, safe='')}")

    def import_contacts(
        self, params: Union[BulkImportContactsParams, Dict[str, Any]]
    ) -> BulkImportResult:
        """
        Bulk import up to 1000 contacts.

        Existing contacts matched by email are updated; new ones are created.

        Args:
            params: Must include ``contacts`` list. Optional ``audience_id``
                to add all imported contacts to an audience.

        Returns:
            BulkImportResult with ``created``, ``updated``, and ``total`` counts.

        Example::

            result = sendry.contacts.import_contacts({
                "contacts": [
                    {"email": "alice@example.com", "first_name": "Alice"},
                    {"email": "bob@example.com", "first_name": "Bob"},
                ],
                "audience_id": "aud_abc123",
            })
            print(f"Created: {result['created']}, Updated: {result['updated']}")
        """
        return self._client.post("/v1/contacts/import", dict(params))


class AsyncContacts:
    """
    Asynchronous contacts resource.

    Access via ``async_sendr.contacts``.
    """

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def create(self, params: Union[CreateContactParams, Dict[str, Any]]) -> Contact:
        """Create a contact. See :meth:`Contacts.create`."""
        return await self._client.post("/v1/contacts", dict(params))

    async def list(
        self, params: Optional[Union[ListContactsParams, Dict[str, Any]]] = None
    ) -> PaginatedResponse:
        """List contacts. See :meth:`Contacts.list`."""
        return await self._client.get("/v1/contacts", dict(params) if params else None)

    async def get(self, contact_id: str) -> Contact:
        """Get a contact. See :meth:`Contacts.get`."""
        return await self._client.get(f"/v1/contacts/{quote(contact_id, safe='')}")

    async def update(
        self, contact_id: str, params: Union[UpdateContactParams, Dict[str, Any]]
    ) -> Contact:
        """Update a contact. See :meth:`Contacts.update`."""
        return await self._client.put(
            f"/v1/contacts/{quote(contact_id, safe='')}", dict(params)
        )

    async def remove(self, contact_id: str) -> DeleteResponse:
        """Delete a contact. See :meth:`Contacts.remove`."""
        return await self._client.delete(f"/v1/contacts/{quote(contact_id, safe='')}")

    async def import_contacts(
        self, params: Union[BulkImportContactsParams, Dict[str, Any]]
    ) -> BulkImportResult:
        """Bulk import contacts. See :meth:`Contacts.import_contacts`."""
        return await self._client.post("/v1/contacts/import", dict(params))


__all__ = ["Contacts", "AsyncContacts"]
