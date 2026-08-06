"""Mock provider."""

from app.providers.provider import Provider


class MockProvider(Provider):
    """Testing provider."""

    def __init__(self):
        super().__init__(name="mock")

    def generate(self, prompt: str) -> str:
        return f"Mock response: {prompt}"
