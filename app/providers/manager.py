"""Provider manager."""

from __future__ import annotations

from collections.abc import Iterator

from app.providers.base import BaseProvider
from app.providers.models import (
    ChatRequest,
    ChatResponse,
)
from app.providers.provider_info import ProviderInfo
from app.providers.stream import ChatChunk


class ProviderManager:
    """Manage AI providers and route requests."""

    def __init__(self) -> None:
        self._providers: dict[str, BaseProvider] = {}
        self._active: str | None = None

    def register(
        self,
        provider: BaseProvider,
    ) -> None:
        """Register a provider."""

        self._providers[provider.name] = provider

        if self._active is None:
            self._active = provider.name

    def get(
        self,
        name: str,
    ) -> BaseProvider:
        """Return a provider by name."""

        try:
            return self._providers[name]
        except KeyError as exc:
            raise KeyError(
                f"Unknown provider: {name}"
            ) from exc

    def remove(
        self,
        name: str,
    ) -> None:
        """Remove a provider."""

        self._providers.pop(name, None)

        if self._active == name:
            self._active = next(
                iter(self._providers),
                None,
            )

    def list_providers(
        self,
    ) -> list[str]:
        """Return registered provider names."""

        return sorted(self._providers)

    def set_active(
        self,
        name: str,
    ) -> None:
        """Select the active provider."""

        if name not in self._providers:
            raise KeyError(
                f"Unknown provider: {name}"
            )

        self._active = name

    def active(
        self,
    ) -> BaseProvider:
        """Return the active provider."""

        if self._active is None:
            raise RuntimeError(
                "No active provider."
            )

        return self._providers[self._active]

    def resolve(
        self,
        provider_name: str | None = None,
    ) -> BaseProvider:
        """Resolve a provider by name or return the active provider."""

        if provider_name is None:
            return self.active()

        return self.get(provider_name)

    def chat(
        self,
        request: ChatRequest,
    ) -> ChatResponse:
        """Send a chat request through the selected provider."""

        provider_name = request.metadata.get(
            "provider",
        )

        if provider_name is not None and not isinstance(
            provider_name,
            str,
        ):
            raise ValueError(
                "Request provider must be a string."
            )

        provider = self.resolve(provider_name)

        return provider.chat(request)

    def stream(
        self,
        request: ChatRequest,
    ) -> Iterator[ChatChunk]:
        """Stream a chat request through the selected provider."""

        provider_name = request.metadata.get(
            "provider",
        )

        if provider_name is not None and not isinstance(
            provider_name,
            str,
        ):
            raise ValueError(
                "Request provider must be a string."
            )

        provider = self.resolve(provider_name)

        return provider.stream_chat(request)

    def health(
        self,
    ) -> dict[str, bool]:
        """Return provider health."""

        return {
            name: provider.health()
            for name, provider
            in self._providers.items()
        }

    def summary(
        self,
    ) -> list[ProviderInfo]:
        """Return provider metadata."""

        return [
            ProviderInfo(
                name=provider.name,
                active=provider.name == self._active,
                healthy=provider.health(),
                models=provider.models(),
                capabilities=provider.capabilities,
            )
            for provider in self._providers.values()
        ]
