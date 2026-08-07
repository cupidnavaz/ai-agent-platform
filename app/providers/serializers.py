"""Provider serializers."""

from __future__ import annotations

from app.providers.models import (
    ChatRequest,
    ChatResponse,
)


class OpenAISerializer:
    """Serialize OpenAI requests and responses."""

    @staticmethod
    def request(
        request: ChatRequest,
        model: str,
    ) -> dict:
        """Convert ChatRequest to OpenAI payload."""

        return {
            "model": model,
            "messages": [
                {
                    "role": message.role,
                    "content": message.content,
                }
                for message in request.messages
            ],
            "temperature": request.temperature,
        }

    @staticmethod
    def response(
        payload: dict,
    ) -> ChatResponse:
        """Convert OpenAI JSON to ChatResponse."""

        choice = payload["choices"][0]

        return ChatResponse(
            content=choice["message"]["content"],
            model=payload.get("model", ""),
            usage=payload.get("usage", {}),
        )
