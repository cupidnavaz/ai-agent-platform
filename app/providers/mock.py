"""Mock AI provider."""

from app.providers.provider import Provider


class MockProvider(Provider):
    """Simple mock provider."""

    def __init__(self):
        super().__init__("mock")

    def chat(self, messages: list[dict[str, str]]) -> str:
        user_message = messages[-1]["content"]
        return f"Mock response: {user_message}"
