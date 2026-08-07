"""OpenAI provider."""

from __future__ import annotations

from app.providers.base import BaseProvider
from app.providers.models import (
    ChatRequest,
    ChatResponse,
    ProviderCapabilities,
)
from app.providers.openai_client import OpenAIClient
from app.providers.openai_config import OpenAIConfig
from app.providers.serializers import OpenAISerializer


class OpenAIProvider(BaseProvider):
    """OpenAI implementation."""

    def __init__(
        self,
        config: OpenAIConfig | None = None,
        client: OpenAIClient | None = None,
    ) -> None:
        """Initialize the provider."""

        if client is not None:
            self.client = client
            self.model = client.config.model
            return

        if config is None:
            raise ValueError(
                "An OpenAIConfig or OpenAIClient must be provided."
            )

        self.model = config.model
        self.client = OpenAIClient(config)

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
