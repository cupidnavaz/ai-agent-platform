"""Dependency injection container."""

from app.agents.assistant import Assistant
from app.providers.provider import Provider


class Container:
    """Simple service container."""

    def __init__(self, provider: Provider):
        self.provider = provider

    def assistant(self) -> Assistant:
        return Assistant(
            provider=self.provider,
        )
