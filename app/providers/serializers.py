"""Provider serializers."""

from __future__ import annotations

from app.providers.errors import ProviderResponseError
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
        """Convert ChatRequest to an OpenAI payload."""

        payload = {
            "model": request.model or model,
            "messages": [
                {
                    "role": message.role,
                    "content": message.content,
                }
                for message in request.messages
            ],
        }

        if request.temperature is not None:
            payload["temperature"] = request.temperature

        if request.max_tokens is not None:
            payload["max_tokens"] = request.max_tokens

        return payload

    @staticmethod
    def response(
        payload: dict,
    ) -> ChatResponse:
        """Convert OpenAI JSON to ChatResponse."""

        try:
            choice = payload["choices"][0]

            return ChatResponse(
                content=choice["message"]["content"],
                model=payload.get("model", ""),
                usage=payload.get("usage", {}),
            )

        except (KeyError, IndexError, TypeError) as exc:
            raise ProviderResponseError(
                "Malformed OpenAI response."
            ) from exc
