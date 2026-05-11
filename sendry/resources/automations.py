"""
Automations resource — automations, steps, and runs.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Union
from urllib.parse import quote

from .._client import AsyncHttpClient, HttpClient
from .._types import (
    AddAutomationStepParams,
    Automation,
    AutomationRun,
    AutomationRunStep,
    AutomationStep,
    CreateAutomationParams,
    CreateAutomationRunParams,
    DeleteResponse,
    ListAutomationRunsParams,
    ListAutomationsParams,
    PaginatedResponse,
    UpdateAutomationParams,
    UpdateAutomationStepParams,
)


class Automations:
    """
    Synchronous automations resource.

    Access via ``sendry.automations``.
    """

    def __init__(self, client: HttpClient) -> None:
        self._client = client

    # -------- Automations --------

    def list(
        self,
        params: Optional[Union[ListAutomationsParams, Dict[str, Any]]] = None,
    ) -> PaginatedResponse:
        """List automations with optional pagination and status filter."""
        return self._client.get("/v1/automations", dict(params) if params else None)

    def get(self, automation_id: str) -> Automation:
        """Get an automation by ID."""
        return self._client.get(f"/v1/automations/{quote(automation_id, safe='')}")

    def create(
        self, params: Union[CreateAutomationParams, Dict[str, Any]]
    ) -> Automation:
        """Create a new automation."""
        return self._client.post("/v1/automations", dict(params))

    def update(
        self,
        automation_id: str,
        params: Union[UpdateAutomationParams, Dict[str, Any]],
    ) -> Automation:
        """Update an automation."""
        return self._client.patch(
            f"/v1/automations/{quote(automation_id, safe='')}", dict(params)
        )

    def remove(self, automation_id: str) -> DeleteResponse:
        """Delete an automation."""
        return self._client.delete(
            f"/v1/automations/{quote(automation_id, safe='')}"
        )

    def activate(self, automation_id: str) -> Automation:
        """Activate an automation."""
        return self._client.post(
            f"/v1/automations/{quote(automation_id, safe='')}/activate"
        )

    def pause(self, automation_id: str) -> Automation:
        """Pause an automation."""
        return self._client.post(
            f"/v1/automations/{quote(automation_id, safe='')}/pause"
        )

    def archive(self, automation_id: str) -> Automation:
        """Archive an automation."""
        return self._client.post(
            f"/v1/automations/{quote(automation_id, safe='')}/archive"
        )

    # -------- Steps --------

    def list_steps(self, automation_id: str) -> Dict[str, List[AutomationStep]]:
        """List all steps in an automation."""
        return self._client.get(
            f"/v1/automations/{quote(automation_id, safe='')}/steps"
        )

    def add_step(
        self,
        automation_id: str,
        params: Union[AddAutomationStepParams, Dict[str, Any]],
    ) -> AutomationStep:
        """Add a step to an automation."""
        return self._client.post(
            f"/v1/automations/{quote(automation_id, safe='')}/steps", dict(params)
        )

    def update_step(
        self,
        automation_id: str,
        step_id: str,
        params: Union[UpdateAutomationStepParams, Dict[str, Any]],
    ) -> AutomationStep:
        """Update a step in an automation."""
        return self._client.patch(
            f"/v1/automations/{quote(automation_id, safe='')}/steps/"
            f"{quote(step_id, safe='')}",
            dict(params),
        )

    def delete_step(self, automation_id: str, step_id: str) -> DeleteResponse:
        """Delete a step from an automation."""
        return self._client.delete(
            f"/v1/automations/{quote(automation_id, safe='')}/steps/"
            f"{quote(step_id, safe='')}"
        )

    # -------- Runs --------

    def list_runs(
        self,
        automation_id: str,
        params: Optional[Union[ListAutomationRunsParams, Dict[str, Any]]] = None,
    ) -> PaginatedResponse:
        """List runs for an automation."""
        return self._client.get(
            f"/v1/automations/{quote(automation_id, safe='')}/runs",
            dict(params) if params else None,
        )

    def get_run(self, automation_id: str, run_id: str) -> AutomationRun:
        """Get a single automation run."""
        return self._client.get(
            f"/v1/automations/{quote(automation_id, safe='')}/runs/"
            f"{quote(run_id, safe='')}"
        )

    def list_run_steps(
        self, automation_id: str, run_id: str
    ) -> Dict[str, List[AutomationRunStep]]:
        """List step executions for an automation run."""
        return self._client.get(
            f"/v1/automations/{quote(automation_id, safe='')}/runs/"
            f"{quote(run_id, safe='')}/steps"
        )

    def cancel_run(self, automation_id: str, run_id: str) -> AutomationRun:
        """Cancel an in-progress automation run."""
        return self._client.post(
            f"/v1/automations/{quote(automation_id, safe='')}/runs/"
            f"{quote(run_id, safe='')}/cancel"
        )

    def create_run(
        self,
        automation_id: str,
        params: Union[CreateAutomationRunParams, Dict[str, Any]],
    ) -> AutomationRun:
        """Create a manual run for an automation."""
        return self._client.post(
            f"/v1/automations/{quote(automation_id, safe='')}/runs", dict(params)
        )


class AsyncAutomations:
    """
    Asynchronous automations resource.

    Access via ``async_sendr.automations``.
    """

    def __init__(self, client: AsyncHttpClient) -> None:
        self._client = client

    # -------- Automations --------

    async def list(
        self,
        params: Optional[Union[ListAutomationsParams, Dict[str, Any]]] = None,
    ) -> PaginatedResponse:
        """List automations. See :meth:`Automations.list`."""
        return await self._client.get(
            "/v1/automations", dict(params) if params else None
        )

    async def get(self, automation_id: str) -> Automation:
        """Get automation. See :meth:`Automations.get`."""
        return await self._client.get(
            f"/v1/automations/{quote(automation_id, safe='')}"
        )

    async def create(
        self, params: Union[CreateAutomationParams, Dict[str, Any]]
    ) -> Automation:
        """Create automation. See :meth:`Automations.create`."""
        return await self._client.post("/v1/automations", dict(params))

    async def update(
        self,
        automation_id: str,
        params: Union[UpdateAutomationParams, Dict[str, Any]],
    ) -> Automation:
        """Update automation. See :meth:`Automations.update`."""
        return await self._client.patch(
            f"/v1/automations/{quote(automation_id, safe='')}", dict(params)
        )

    async def remove(self, automation_id: str) -> DeleteResponse:
        """Delete automation. See :meth:`Automations.remove`."""
        return await self._client.delete(
            f"/v1/automations/{quote(automation_id, safe='')}"
        )

    async def activate(self, automation_id: str) -> Automation:
        """Activate automation. See :meth:`Automations.activate`."""
        return await self._client.post(
            f"/v1/automations/{quote(automation_id, safe='')}/activate"
        )

    async def pause(self, automation_id: str) -> Automation:
        """Pause automation. See :meth:`Automations.pause`."""
        return await self._client.post(
            f"/v1/automations/{quote(automation_id, safe='')}/pause"
        )

    async def archive(self, automation_id: str) -> Automation:
        """Archive automation. See :meth:`Automations.archive`."""
        return await self._client.post(
            f"/v1/automations/{quote(automation_id, safe='')}/archive"
        )

    # -------- Steps --------

    async def list_steps(
        self, automation_id: str
    ) -> Dict[str, List[AutomationStep]]:
        """List steps. See :meth:`Automations.list_steps`."""
        return await self._client.get(
            f"/v1/automations/{quote(automation_id, safe='')}/steps"
        )

    async def add_step(
        self,
        automation_id: str,
        params: Union[AddAutomationStepParams, Dict[str, Any]],
    ) -> AutomationStep:
        """Add step. See :meth:`Automations.add_step`."""
        return await self._client.post(
            f"/v1/automations/{quote(automation_id, safe='')}/steps", dict(params)
        )

    async def update_step(
        self,
        automation_id: str,
        step_id: str,
        params: Union[UpdateAutomationStepParams, Dict[str, Any]],
    ) -> AutomationStep:
        """Update step. See :meth:`Automations.update_step`."""
        return await self._client.patch(
            f"/v1/automations/{quote(automation_id, safe='')}/steps/"
            f"{quote(step_id, safe='')}",
            dict(params),
        )

    async def delete_step(
        self, automation_id: str, step_id: str
    ) -> DeleteResponse:
        """Delete step. See :meth:`Automations.delete_step`."""
        return await self._client.delete(
            f"/v1/automations/{quote(automation_id, safe='')}/steps/"
            f"{quote(step_id, safe='')}"
        )

    # -------- Runs --------

    async def list_runs(
        self,
        automation_id: str,
        params: Optional[Union[ListAutomationRunsParams, Dict[str, Any]]] = None,
    ) -> PaginatedResponse:
        """List runs. See :meth:`Automations.list_runs`."""
        return await self._client.get(
            f"/v1/automations/{quote(automation_id, safe='')}/runs",
            dict(params) if params else None,
        )

    async def get_run(self, automation_id: str, run_id: str) -> AutomationRun:
        """Get run. See :meth:`Automations.get_run`."""
        return await self._client.get(
            f"/v1/automations/{quote(automation_id, safe='')}/runs/"
            f"{quote(run_id, safe='')}"
        )

    async def list_run_steps(
        self, automation_id: str, run_id: str
    ) -> Dict[str, List[AutomationRunStep]]:
        """List run steps. See :meth:`Automations.list_run_steps`."""
        return await self._client.get(
            f"/v1/automations/{quote(automation_id, safe='')}/runs/"
            f"{quote(run_id, safe='')}/steps"
        )

    async def cancel_run(
        self, automation_id: str, run_id: str
    ) -> AutomationRun:
        """Cancel run. See :meth:`Automations.cancel_run`."""
        return await self._client.post(
            f"/v1/automations/{quote(automation_id, safe='')}/runs/"
            f"{quote(run_id, safe='')}/cancel"
        )

    async def create_run(
        self,
        automation_id: str,
        params: Union[CreateAutomationRunParams, Dict[str, Any]],
    ) -> AutomationRun:
        """Create manual run. See :meth:`Automations.create_run`."""
        return await self._client.post(
            f"/v1/automations/{quote(automation_id, safe='')}/runs", dict(params)
        )


__all__ = ["Automations", "AsyncAutomations"]
