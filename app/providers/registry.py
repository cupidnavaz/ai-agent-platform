"""Provider registry."""

from app.providers.base import BaseProvider


class ProviderRegistry:
    """Registry for AI providers."""

    def __init__(self):
        self._providers: dict[str, BaseProvider] = {}

    def register(
        self,
        provider: BaseProvider,
    ) -> None:
        """Register a provider."""
        self._providers[provider.name] = provider

    def get(
        self,
        name: str,
    ) -> BaseProvider:
        """Get a provider by name."""
        return self._providers[name]

    def remove(
        self,
        name: str,
    ) -> None:
        """Remove a provider."""
        self._providers.pop(name, None)

    def list(
        self,
    ) -> list[str]:
        """List registered providers."""
        return sorted(self._providers.keys())
