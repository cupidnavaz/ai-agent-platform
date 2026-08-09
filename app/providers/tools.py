"""Provider-neutral tool registry."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from app.providers.models import (
    ToolCall,
    ToolDefinition,
    ToolResult,
)


ToolHandler = Callable[..., Any]


class ToolRegistry:
    """Register and execute application tools."""

    def __init__(self) -> None:
        self._definitions: dict[str, ToolDefinition] = {}
        self._handlers: dict[str, ToolHandler] = {}

    def register(
        self,
        definition: ToolDefinition,
        handler: ToolHandler,
    ) -> None:
        """Register a tool definition and its handler."""

        if not definition.name:
            raise ValueError(
                "Tool name must not be empty."
            )

        if definition.name in self._definitions:
            raise ValueError(
                f"Tool already registered: {definition.name}"
            )

        self._definitions[definition.name] = definition
        self._handlers[definition.name] = handler

    def get(
        self,
        name: str,
    ) -> ToolDefinition:
        """Return a registered tool definition."""

        try:
            return self._definitions[name]
        except KeyError as exc:
            raise KeyError(
                f"Tool not found: {name}"
            ) from exc

    def definitions(self) -> list[ToolDefinition]:
        """Return all registered tool definitions."""

        return list(self._definitions.values())

    def execute(
        self,
        call: ToolCall,
    ) -> ToolResult:
        """Execute a tool call and normalize its result."""

        try:
            handler = self._handlers[call.name]
        except KeyError as exc:
            raise KeyError(
                f"Tool not found: {call.name}"
            ) from exc

        try:
            result = handler(**call.arguments)
        except Exception as exc:
            raise RuntimeError(
                f"Tool execution failed: {call.name}"
            ) from exc

        if isinstance(result, str):
            content = result
        else:
            content = str(result)

        return ToolResult(
            tool_call_id=call.id,
            content=content,
        )
