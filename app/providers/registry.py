"""Provider registry."""

from app.providers.provider import Provider


class ProviderRegistry:
    """Stores AI providers."""

    def __init__(self):
        self._providers: dict[str, Provider] = {}

    def register(self, provider: Provider):
        self._providers[provider.name] = provider

    def get(self, name: str):
        return self._providers.get(name)

    def list(self):
        return sorted(self._providers.keys())

    def remove(self, name: str):
        return self._providers.pop(name, None) is not None
