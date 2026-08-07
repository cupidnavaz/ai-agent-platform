"""Provider information models."""

from dataclasses import dataclass

from app.providers.models import ProviderCapabilities


@dataclass(slots=True)
class ProviderInfo:
    """Information about a registered provider."""

    name: str

    active: bool

    healthy: bool

    models: list[str]

    capabilities: ProviderCapabilities
