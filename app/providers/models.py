"""Shared provider models."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Message:
    """A chat message."""

    role: str
    content: str


@dataclass(slots=True)
class ChatRequest:
    """Request sent to a provider."""

    messages: list[Message]
    model: str | None = None
    temperature: float = 0.7
    max_tokens: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ChatResponse:
    """Response returned by a provider."""

    content: str
    model: str = ""
    usage: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ProviderCapabilities:
    """Provider feature flags."""

    chat: bool = True
    streaming: bool = False
    vision: bool = False
    tool_calling: bool = False
    embeddings: bool = False
