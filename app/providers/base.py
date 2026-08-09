"""Base provider interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator

from app.providers.models import (
    ChatRequest,
    ChatResponse,
    ProviderCapabilities,
)
from app.providers.stream import ChatChunk


class BaseProvider(ABC):
    """Abstract provider interface."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the provider name."""

        raise NotImplementedError

    @property
    def capabilities(self) -> ProviderCapabilities:
        """Return provider capabilities."""

        return ProviderCapabilities()

    @abstractmethod
    def chat(
        self,
        request: ChatRequest,
    ) -> ChatResponse:
        """Send a chat request."""

        raise NotImplementedError

    def stream_chat(
        self,
        request: ChatRequest,
    ) -> Iterator[ChatChunk]:
        """Stream a chat request."""

        raise NotImplementedError(
            f"Provider '{self.name}' "
            "does not support streaming."
        )

    def models(self) -> list[str]:
        """Return supported models."""

        return []

    def health(self) -> bool:
        """Return provider health status."""

        return True
