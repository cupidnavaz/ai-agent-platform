"""Dependency injection container."""

from app.agents.assistant import Assistant
from app.providers.base import BaseProvider


class Container:
    """Simple dependency injection container."""

    def __init__(
        self,
        provider: BaseProvider,
    ) -> None:
        self.provider = provider

    def assistant(self) -> Assistant:
        """Create a new assistant instance."""
        return Assistant(
            provider=self.provider,
        )
