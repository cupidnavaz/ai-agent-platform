"""Dependency injection container."""

from app.agents.assistant import Assistant
from app.providers.base import BaseProvider


class Container:
    """Simple service container."""

    def __init__(
        self,
        provider: BaseProvider,
    ):
        self.provider = provider

    def assistant(self) -> Assistant:
        return Assistant(
            provider=self.provider,
        )
