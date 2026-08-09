"""Shared provider models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Message:
    """A chat message."""

    role: str
    content: str
    tool_call_id: str | None = None
    tool_calls: list[ToolCall] = field(default_factory=list)


@dataclass(slots=True)
class ToolDefinition:
    """Definition of a tool available to a provider."""

    name: str
    description: str
    parameters: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ToolCall:
    """Tool call requested by a model."""

    id: str
    name: str
    arguments: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ToolResult:
    """Result returned after executing a tool."""

    tool_call_id: str
    content: str


@dataclass(slots=True)
class ChatRequest:
    """Request sent to a provider."""

    messages: list[Message]
    model: str | None = None
    temperature: float = 0.7
    max_tokens: int | None = None
    tools: list[ToolDefinition] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ChatResponse:
    """Response returned by a provider."""

    content: str
    model: str = ""
    usage: dict[str, Any] = field(default_factory=dict)
    tool_calls: list[ToolCall] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ProviderCapabilities:
    """Provider feature flags."""

    chat: bool = True
    streaming: bool = False
    vision: bool = False
    tool_calling: bool = False
    embeddings: bool = False
