"""Provider base class."""

from abc import ABC, abstractmethod


class Provider(ABC):
    """Base AI provider."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def chat(self, messages: list[dict[str, str]]) -> str:
        """Generate a response from a conversation."""
        raise NotImplementedError
