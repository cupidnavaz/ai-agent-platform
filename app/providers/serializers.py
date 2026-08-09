"""Provider serializers."""

from __future__ import annotations

import json

from app.providers.errors import ProviderResponseError
from app.providers.models import (
    ChatRequest,
    ChatResponse,
    Message,
    ToolCall,
)


class OpenAISerializer:
    """Serialize OpenAI requests and responses."""

    @staticmethod
    def request(
        request: ChatRequest,
        model: str,
    ) -> dict:
        """Convert ChatRequest to OpenAI payload."""

        messages = []

        for message in request.messages:
            serialized = {
                "role": message.role,
                "content": message.content,
            }

            if message.tool_call_id is not None:
                serialized["tool_call_id"] = message.tool_call_id

            if message.tool_calls:
                serialized["tool_calls"] = [
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.name,
                            "arguments": json.dumps(
                                tool_call.arguments,
                            ),
                        },
                    }
                    for tool_call in message.tool_calls
                ]

            messages.append(serialized)

        payload = {
            "model": request.model or model,
            "messages": messages,
            "temperature": request.temperature,
        }

        if request.max_tokens is not None:
            payload["max_tokens"] = request.max_tokens

        if request.tools:
            payload["tools"] = [
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.parameters,
                    },
                }
                for tool in request.tools
            ]

        return payload

    @staticmethod
    def response(
        payload: dict,
    ) -> ChatResponse:
        """Convert OpenAI JSON to ChatResponse."""

        try:
            choice = payload["choices"][0]
            message = choice["message"]
        except (
            KeyError,
            IndexError,
            TypeError,
        ) as exc:
            raise ProviderResponseError(
                "Invalid OpenAI response payload."
            ) from exc

        tool_calls: list[ToolCall] = []

        for raw_tool_call in message.get(
            "tool_calls",
            [],
        ):
            try:
                function = raw_tool_call["function"]

                arguments = function.get(
                    "arguments",
                    {},
                )

                if isinstance(arguments, str):
                    arguments = json.loads(arguments)

                if not isinstance(arguments, dict):
                    raise ProviderResponseError(
                        "Tool call arguments must be an object."
                    )

                tool_calls.append(
                    ToolCall(
                        id=raw_tool_call.get(
                            "id",
                            "",
                        ),
                        name=function["name"],
                        arguments=arguments,
                    )
                )

            except (
                KeyError,
                TypeError,
                json.JSONDecodeError,
            ) as exc:
                raise ProviderResponseError(
                    "Invalid OpenAI tool call payload."
                ) from exc

        return ChatResponse(
            content=message.get(
                "content",
            ) or "",
            model=payload.get(
                "model",
                "",
            ),
            usage=payload.get(
                "usage",
                {},
            ),
            tool_calls=tool_calls,
        )
