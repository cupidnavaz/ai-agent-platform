"""OpenAI provider."""

from __future__ import annotations

from collections.abc import Iterator

from app.providers.base import BaseProvider
from app.providers.models import (
    ChatRequest,
    ChatResponse,
    ProviderCapabilities,
)
from app.providers.openai_client import OpenAIClient
from app.providers.serializers import OpenAISerializer
from app.providers.stream import ChatChunk


class OpenAIProvider(BaseProvider):
    """OpenAI implementation."""

    def __init__(
        self,
        config,
        client: OpenAIClient | None = None,
    ) -> None:
        """Initialize the provider."""

        self.config = config
        self.model = config.model

        if client is not None:
            self.client = client
        else:
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

    def stream_chat(
        self,
        request: ChatRequest,
    ) -> Iterator[ChatChunk]:
        """Stream chat response chunks."""

        payload = OpenAISerializer.request(
            request,
            self.model,
        )

        payload["stream"] = True

        for event in self.client.stream(
            "chat/completions",
            payload,
        ):
            choices = event.get("choices", [])

            if not choices:
                continue

            choice = choices[0]
            delta = choice.get("delta", {})

            content = delta.get("content")

            if content:
                yield ChatChunk(
                    content=content,
                )

            if choice.get("finish_reason") is not None:
                yield ChatChunk(
                    content="",
                    finished=True,
                )

    def models(self) -> list[str]:
        return [self.model]

    def health(self) -> bool:
        return self.client.health()
