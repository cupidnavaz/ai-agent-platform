"""Base Tool class."""

from dataclasses import dataclass


@dataclass
class Tool:
    """Represents a tool an AI agent can use."""

    name: str
    description: str = ""

    def run(self, *args, **kwargs):
        raise NotImplementedError("Tool must implement run().")
