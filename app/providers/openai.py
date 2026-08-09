"""OpenAI provider."""

from __future__ import annotations

from collections.abc import Iterator

from app.providers.base import BaseProvider
from app.providers.models import (
    ChatRequest,
    ChatResponse,
    Message,
    ProviderCapabilities,
)
from app.providers.openai_client import OpenAIClient
from app.providers.serializers import OpenAISerializer
from app.providers.stream import ChatChunk
from app.providers.tools import ToolRegistry


class OpenAIProvider(BaseProvider):
    """OpenAI provider implementation."""

    def __init__(
        self,
        config,
        client: OpenAIClient | None = None,
        tool_registry: ToolRegistry | None = None,
    ) -> None:
        """Initialize the provider."""

        self.config = config
        self.model = config.model
        self.tool_registry = tool_registry

        self.client = (
            client
            if client is not None
            else OpenAIClient(config)
        )

    @property
    def name(self) -> str:
        """Return provider name."""

        return "openai"

    @property
    def capabilities(self) -> ProviderCapabilities:
        """Return provider capabilities."""

        return ProviderCapabilities(
            chat=True,
            streaming=True,
            vision=True,
            tool_calling=True,
            embeddings=True,
        )

    def models(self) -> list[str]:
        """Return models supported by this provider."""

        return [self.model]

    def health(self) -> bool:
        """Return provider health status."""

        return self.client.health()

    def chat(
        self,
        request: ChatRequest,
    ) -> ChatResponse:
        """Send a chat request and execute requested tools."""

        messages = list(request.messages)

        while True:
            current_request = ChatRequest(
                messages=messages,
                model=request.model,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                tools=self._request_tools(request),
                metadata=request.metadata,
            )

            payload = OpenAISerializer.request(
                current_request,
                self.model,
            )

            response = self.client.post(
                "chat/completions",
                payload,
            )

            chat_response = OpenAISerializer.response(
                response.body,
            )

            if not chat_response.tool_calls:
                return chat_response

            if self.tool_registry is None:
                return chat_response

            messages.append(
                Message(
                    role="assistant",
                    content=chat_response.content,
                    tool_calls=chat_response.tool_calls,
                )
            )

            for tool_call in chat_response.tool_calls:
                result = self.tool_registry.execute(
                    tool_call,
                )

                messages.append(
                    Message(
                        role="tool",
                        content=result.content,
                        tool_call_id=result.tool_call_id,
                    )
                )

    def stream_chat(
        self,
        request: ChatRequest,
    ) -> Iterator[ChatChunk]:
        """Stream an OpenAI chat response."""

        payload = OpenAISerializer.request(
            ChatRequest(
                messages=request.messages,
                model=request.model,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                tools=self._request_tools(request),
                metadata=request.metadata,
            ),
            self.model,
        )

        payload["stream"] = True

        for event in self.client.stream(
            "chat/completions",
            payload,
        ):
            choices = event.get(
                "choices",
                [],
            )

            if not choices:
                continue

            choice = choices[0]

            delta = choice.get(
                "delta",
                {},
            )

            content = delta.get(
                "content",
                "",
            ) or ""

            finished = (
                choice.get(
                    "finish_reason",
                )
                is not None
            )

            yield ChatChunk(
                content=content,
                finished=finished,
            )

    def _request_tools(
        self,
        request: ChatRequest,
    ):
        """Resolve request tools or registered tools."""

        if request.tools:
            return request.tools

        if self.tool_registry is not None:
            return self.tool_registry.definitions()

        return []


if __name__ == "__main__":
    pass
