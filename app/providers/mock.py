"""Mock provider."""

from app.providers.base import BaseProvider
from app.providers.models import (
    ChatRequest,
    ChatResponse,
    ProviderCapabilities,
)


class MockProvider(BaseProvider):

    @property
    def name(self) -> str:
        return "mock"

    @property
    def capabilities(self) -> ProviderCapabilities:
        return ProviderCapabilities(
            chat=True,
            streaming=False,
            vision=False,
            tool_calling=False,
            embeddings=False,
        )

    def chat(
        self,
        request: ChatRequest,
    ) -> ChatResponse:

        last = request.messages[-1].content

        return ChatResponse(
            content=f"Mock response: {last}",
            model="mock-v1",
        )

    def models(self) -> list[str]:
        return ["mock-v1"]
