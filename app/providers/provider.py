"""Base Provider class."""

from dataclasses import dataclass


@dataclass
class Provider:
    """Base AI provider."""

    name: str

    def generate(self, prompt: str) -> str:
        raise NotImplementedError("Provider must implement generate().")
