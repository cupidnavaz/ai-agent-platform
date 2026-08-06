"""Core Agent model."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Agent:
    """Represents an AI agent."""

    name: str
    description: str = ""
    model: str = "default"
    tools: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def info(self) -> dict[str, Any]:
        """Return agent information."""
        return {
            "name": self.name,
            "description": self.description,
            "model": self.model,
            "tools": self.tools,
            "metadata": self.metadata,
        }
