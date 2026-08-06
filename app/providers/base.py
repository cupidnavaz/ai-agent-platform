"""Base provider interface."""

from abc import ABC, abstractmethod

from app.providers.models import (
    ChatRequest,
    ChatResponse,
    ProviderCapabilities,
)


class BaseProvider(ABC):
    """Abstract provider interface."""

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @property
    def capabilities(self) -> ProviderCapabilities:
        return ProviderCapabilities()

    @abstractmethod
    def chat(
        self,
        request: ChatRequest,
    ) -> ChatResponse:
        raise NotImplementedError

    def stream(
        self,
        request: ChatRequest,
    ):
        raise NotImplementedError(
            "Streaming is not implemented."
        )

    def models(self) -> list[str]:
        return []

    def health(self) -> bool:
        return True
