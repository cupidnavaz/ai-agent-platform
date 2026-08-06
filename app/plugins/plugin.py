"""Plugin base class."""

from abc import ABC, abstractmethod


class Plugin(ABC):
    """Base class for all plugins."""

    def __init__(
        self,
        name: str,
        description: str = "",
    ) -> None:
        self.name = name
        self.description = description

    @abstractmethod
    def setup(self) -> None:
        """Called when the plugin is loaded."""
        raise NotImplementedError
