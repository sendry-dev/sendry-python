"""
Templates resource — create, list, get, update, remove, render.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Union
from urllib.parse import quote

from .._client import AsyncHttpClient, HttpClient
from .._types import (
    CreateTemplateParams,
    DeleteResponse,
    PaginatedResponse,
    PaginationParams,
    RenderTemplateParams,
    RenderTemplateResponse,
    Template,
    UpdateTemplateParams,
)


class Templates:
    """
    Synchronous templates resource.

    Access via ``sendry.templates``.
    """

    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def create(self, params: Union[CreateTemplateParams, Dict[str, Any]]) -> Template:
        """
        Create a new email template.

        Args:
            params: Template configuration — ``name`` is required.
                Include ``subject``, ``html``, ``engine``, and ``variables``
                as needed.

        Returns:
            The created Template object.

        Example::

            template = sendry.templates.create({
                "name": "Welcome Email",
                "subject": "Welcome, {{name}}!",
                "html": "<h1>Hello {{name}}</h1>",
            })
        """
        return self._client.post("/v1/templates", dict(params))

    def list(self, params: Optional[Union[PaginationParams, Dict[str, Any]]] = None) -> PaginatedResponse:
        """
        List all templates with optional pagination.

        Args:
            params: Optional ``limit`` and ``cursor``.

        Returns:
            PaginatedResponse of Template objects.
        """
        return self._client.get("/v1/templates", dict(params) if params else None)

    def get(self, template_id: str) -> Template:
        """
        Get a template by ID.

        Args:
            template_id: The template ID (e.g. ``tmpl_abc123``).

        Returns:
            Full Template object including HTML and variable definitions.
        """
        return self._client.get(f"/v1/templates/{quote(template_id, safe='')}")

    def update(
        self, template_id: str, params: Union[UpdateTemplateParams, Dict[str, Any]]
    ) -> Template:
        """
        Update a template.

        Args:
            template_id: The template ID.
            params: Fields to update. All fields are optional.

        Returns:
            Updated Template object.

        Example::

            updated = sendry.templates.update("tmpl_abc123", {
                "subject": "Updated: Welcome, {{name}}!",
            })
        """
        return self._client.put(f"/v1/templates/{quote(template_id, safe='')}", dict(params))

    def remove(self, template_id: str) -> DeleteResponse:
        """
        Delete a template.

        Args:
            template_id: The template ID.

        Returns:
            DeleteResponse acknowledging the deletion.
        """
        return self._client.delete(f"/v1/templates/{quote(template_id, safe='')}")

    def render(
        self,
        template_id: str,
        params: Optional[Union[RenderTemplateParams, Dict[str, Any]]] = None,
    ) -> RenderTemplateResponse:
        """
        Render a saved template with the given variable values.

        Args:
            template_id: The template ID.
            params: Optional ``variables`` dict for substitution.

        Returns:
            RenderTemplateResponse with ``html`` and ``text`` strings.

        Example::

            rendered = sendry.templates.render("tmpl_abc123", {
                "variables": {"name": "Alice", "plan": "Pro"},
            })
            print(rendered["html"])
        """
        return self._client.post(
            f"/v1/templates/{quote(template_id, safe='')}/render",
            dict(params) if params else {},
        )

    def list_starters(self) -> Dict[str, List[Any]]:
        """
        List all pre-built starter templates.

        Returns:
            Dict with a ``data`` key containing a list of starter templates.
        """
        return self._client.get("/v1/templates/starters")

    def list_visual_starters(self) -> Dict[str, List[Any]]:
        """
        List all available visual (block-based) starter templates.

        Returns:
            Dict with a ``data`` key containing a list of visual starter summaries.
        """
        return self._client.get("/v1/templates/visual-starters")

    def get_visual_starter(self, starter_id: str) -> Dict[str, Any]:
        """
        Get the full design JSON for a visual starter template.

        Args:
            starter_id: The visual starter ID (e.g. ``welcome-blocks``).

        Returns:
            Dict containing the full block design payload.
        """
        return self._client.get(f"/v1/templates/visual-starters/{quote(starter_id, safe='')}")

    def compile_blocks(self, params: Dict[str, Any]) -> RenderTemplateResponse:
        """
        Compile a visual block design JSON to email-safe HTML.

        Args:
            params: Dict with ``design`` (block JSON) and optional ``variables``.

        Returns:
            RenderTemplateResponse with compiled ``html`` and ``text``.
        """
        return self._client.post("/v1/templates/compile-blocks", params)

    def render_adhoc(self, params: Dict[str, Any]) -> RenderTemplateResponse:
        """
        Render arbitrary template HTML without saving it first.

        Args:
            params: Dict with ``html``, optional ``engine``, and ``variables``.

        Returns:
            RenderTemplateResponse with rendered ``html`` and ``text``.

        Example::

            result = sendry.templates.render_adhoc({
                "html": "<h1>Hello {{name}}</h1>",
                "variables": {"name": "Bob"},
            })
        """
        return self._client.post("/v1/templates/render", params)


class AsyncTemplates:
    """
    Asynchronous templates resource.

    Access via ``async_sendr.templates``.
    """

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    async def create(self, params: Union[CreateTemplateParams, Dict[str, Any]]) -> Template:
        """Create a template. See :meth:`Templates.create`."""
        return await self._client.post("/v1/templates", dict(params))

    async def list(
        self, params: Optional[Union[PaginationParams, Dict[str, Any]]] = None
    ) -> PaginatedResponse:
        """List templates. See :meth:`Templates.list`."""
        return await self._client.get("/v1/templates", dict(params) if params else None)

    async def get(self, template_id: str) -> Template:
        """Get a template. See :meth:`Templates.get`."""
        return await self._client.get(f"/v1/templates/{quote(template_id, safe='')}")

    async def update(
        self, template_id: str, params: Union[UpdateTemplateParams, Dict[str, Any]]
    ) -> Template:
        """Update a template. See :meth:`Templates.update`."""
        return await self._client.put(
            f"/v1/templates/{quote(template_id, safe='')}", dict(params)
        )

    async def remove(self, template_id: str) -> DeleteResponse:
        """Delete a template. See :meth:`Templates.remove`."""
        return await self._client.delete(f"/v1/templates/{quote(template_id, safe='')}")

    async def render(
        self,
        template_id: str,
        params: Optional[Union[RenderTemplateParams, Dict[str, Any]]] = None,
    ) -> RenderTemplateResponse:
        """Render a template. See :meth:`Templates.render`."""
        return await self._client.post(
            f"/v1/templates/{quote(template_id, safe='')}/render",
            dict(params) if params else {},
        )

    async def list_starters(self) -> Dict[str, List[Any]]:
        """List starter templates. See :meth:`Templates.list_starters`."""
        return await self._client.get("/v1/templates/starters")

    async def list_visual_starters(self) -> Dict[str, List[Any]]:
        """List visual starters. See :meth:`Templates.list_visual_starters`."""
        return await self._client.get("/v1/templates/visual-starters")

    async def get_visual_starter(self, starter_id: str) -> Dict[str, Any]:
        """Get visual starter design. See :meth:`Templates.get_visual_starter`."""
        return await self._client.get(
            f"/v1/templates/visual-starters/{quote(starter_id, safe='')}"
        )

    async def compile_blocks(self, params: Dict[str, Any]) -> RenderTemplateResponse:
        """Compile block design to HTML. See :meth:`Templates.compile_blocks`."""
        return await self._client.post("/v1/templates/compile-blocks", params)

    async def render_adhoc(self, params: Dict[str, Any]) -> RenderTemplateResponse:
        """Render arbitrary HTML. See :meth:`Templates.render_adhoc`."""
        return await self._client.post("/v1/templates/render", params)


__all__ = ["Templates", "AsyncTemplates"]
