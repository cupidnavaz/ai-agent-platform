"""Provider manager."""

from app.providers.base import BaseProvider
from app.providers.provider_info import ProviderInfo


class ProviderManager:
    """Manage AI providers."""

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
        """Return a provider."""

        return self._providers[name]

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

        return sorted(
            self._providers.keys()
        )

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

        providers: list[ProviderInfo] = []

        for provider in self._providers.values():

            providers.append(
                ProviderInfo(
                    name=provider.name,
                    active=(
                        provider.name
                        == self._active
                    ),
                    healthy=provider.health(),
                    models=provider.models(),
                    capabilities=provider.capabilities,
                )
            )

        return providers


# ==========================================================
# FUTURE AI STUDIO FEATURES (Private Roadmap)
#
# - Provider groups
# - Automatic failover
# - Load balancing
# - Cost tracking
# - Provider priorities
# - Rate limiting
# - Provider benchmarking
# - Health dashboard
# - A/B routing
# - Enterprise policy engine
#
# Reserved for future implementation.
# ==========================================================
