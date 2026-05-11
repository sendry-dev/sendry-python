"""
Team resource — list, invite, remove, update_role.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Union
from urllib.parse import quote

from .._client import AsyncHttpClient, HttpClient
from .._types import (
    DeleteResponse,
    InviteTeamMemberParams,
    ListTeamResponse,
    TeamMember,
    UpdateTeamMemberRoleParams,
)


class Team:
    """
    Synchronous team management resource.

    Access via ``sendry.team``.
    """

    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def list(self) -> ListTeamResponse:
        """
        List all team members and seat usage.

        Returns:
            ListTeamResponse with ``data`` (list of TeamMember), ``seats``
            (used/limit/unlimited), and ``plan``.

        Example::

            team = sendry.team.list()
            print(f"Team size: {team['seats']['used']} / {team['seats']['limit']}")
            for member in team["data"]:
                print(member["email"], member["role"])
        """
        return self._client.get("/v1/team")

    def invite(
        self, params: Union[InviteTeamMemberParams, Dict[str, Any]]
    ) -> TeamMember:
        """
        Invite a new team member by email.

        An invitation email is sent to the address. The member appears in the
        list with ``status`` of ``"invited"`` until they accept.

        Args:
            params: Must include ``email``. Optional ``role``
                (defaults to ``"member"``).

        Returns:
            TeamMember record for the invited user.

        Example::

            member = sendry.team.invite({
                "email": "alice@example.com",
                "role": "admin",
            })
            print(f"Invited {member['email']}")
        """
        return self._client.post("/v1/team/invite", dict(params))

    def remove(self, member_id: str) -> DeleteResponse:
        """
        Remove a team member from the organisation.

        Args:
            member_id: The team member ID (e.g. ``tm_abc123``).

        Returns:
            DeleteResponse acknowledging the removal.

        Example::

            sendry.team.remove("tm_abc123")
        """
        return self._client.delete(f"/v1/team/{quote(member_id, safe='')}")

    def update_role(
        self, member_id: str, params: Union[UpdateTeamMemberRoleParams, Dict[str, Any]]
    ) -> TeamMember:
        """
        Update a team member's role.

        Args:
            member_id: The team member ID.
            params: Must include ``role`` (e.g. ``"admin"``, ``"member"``).

        Returns:
            Updated TeamMember record.

        Example::

            sendry.team.update_role("tm_abc123", {"role": "admin"})
        """
        return self._client.put(f"/v1/team/{quote(member_id, safe='')}/role", dict(params))


class AsyncTeam:
    """
    Asynchronous team management resource.

    Access via ``async_sendr.team``.
    """

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def list(self) -> ListTeamResponse:
        """List team members. See :meth:`Team.list`."""
        return await self._client.get("/v1/team")

    async def invite(
        self, params: Union[InviteTeamMemberParams, Dict[str, Any]]
    ) -> TeamMember:
        """Invite a team member. See :meth:`Team.invite`."""
        return await self._client.post("/v1/team/invite", dict(params))

    async def remove(self, member_id: str) -> DeleteResponse:
        """Remove a team member. See :meth:`Team.remove`."""
        return await self._client.delete(f"/v1/team/{quote(member_id, safe='')}")

    async def update_role(
        self, member_id: str, params: Union[UpdateTeamMemberRoleParams, Dict[str, Any]]
    ) -> TeamMember:
        """Update a team member's role. See :meth:`Team.update_role`."""
        return await self._client.put(
            f"/v1/team/{quote(member_id, safe='')}/role", dict(params)
        )


__all__ = ["Team", "AsyncTeam"]
