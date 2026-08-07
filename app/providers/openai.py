"""OpenAI provider."""

from __future__ import annotations

from app.providers.base import BaseProvider
from app.providers.models import (
    ChatRequest,
    ChatResponse,
    ProviderCapabilities,
)
from app.providers.openai_client import OpenAIClient
from app.providers.serializers import OpenAISerializer


class OpenAIProvider(BaseProvider):
    """OpenAI implementation."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "gpt-4.1-mini",
        client: OpenAIClient | None = None,
    ) -> None:
        """Initialize the provider."""

        self.model = model

        if client is not None:
            self.client = client
        else:
            if api_key is None:
                raise ValueError(
                    "An API key or OpenAIClient must be provided."
                )

            self.client = OpenAIClient(api_key)

    @property
    def name(self) -> str:
        return "openai"

    @property
    def capabilities(self) -> ProviderCapabilities:
        return ProviderCapabilities(
            chat=True,
            streaming=True,
            vision=True,
            tool_calling=True,
            embeddings=True,
        )

    def chat(
        self,
        request: ChatRequest,
    ) -> ChatResponse:
        """Send a chat request."""

        payload = OpenAISerializer.request(
            request,
            self.model,
        )

        response = self.client.post(
            "chat/completions",
            payload,
        )

        return OpenAISerializer.response(
            response.body,
        )

    def models(self) -> list[str]:
        return [self.model]

    def health(self) -> bool:
        return self.client.health()
