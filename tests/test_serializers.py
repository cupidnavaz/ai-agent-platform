"""Tests for provider serializers."""

import unittest

from app.providers.errors import ProviderResponseError
from app.providers.models import (
    ChatRequest,
    Message,
    ToolCall,
    ToolDefinition,
)
from app.providers.serializers import OpenAISerializer


class OpenAISerializerTests(unittest.TestCase):
    """OpenAI serializer tests."""

    def test_request(self):
        request = ChatRequest(
            messages=[
                Message(
                    role="user",
                    content="Hello",
                ),
            ],
        )

        payload = OpenAISerializer.request(
            request,
            "gpt-4.1-mini",
        )

        self.assertEqual(
            payload["model"],
            "gpt-4.1-mini",
        )

        self.assertEqual(
            payload["messages"][0]["role"],
            "user",
        )

        self.assertEqual(
            payload["messages"][0]["content"],
            "Hello",
        )

        self.assertEqual(
            payload["temperature"],
            0.7,
        )

    def test_request_custom_model(self):
        request = ChatRequest(
            messages=[
                Message(
                    role="user",
                    content="Hello",
                ),
            ],
            model="gpt-5",
        )

        payload = OpenAISerializer.request(
            request,
            "gpt-4.1-mini",
        )

        self.assertEqual(
            payload["model"],
            "gpt-5",
        )

    def test_request_max_tokens(self):
        request = ChatRequest(
            messages=[
                Message(
                    role="user",
                    content="Hello",
                ),
            ],
            max_tokens=100,
        )

        payload = OpenAISerializer.request(
            request,
            "gpt-4.1-mini",
        )

        self.assertEqual(
            payload["max_tokens"],
            100,
        )

    def test_request_tools(self):
        request = ChatRequest(
            messages=[
                Message(
                    role="user",
                    content="What is the weather?",
                ),
            ],
            tools=[
                ToolDefinition(
                    name="get_weather",
                    description="Get the current weather.",
                    parameters={
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                            },
                        },
                        "required": [
                            "location",
                        ],
                    },
                ),
            ],
        )

        payload = OpenAISerializer.request(
            request,
            "gpt-4.1-mini",
        )

        self.assertEqual(
            len(payload["tools"]),
            1,
        )

        tool = payload["tools"][0]

        self.assertEqual(
            tool["type"],
            "function",
        )

        self.assertEqual(
            tool["function"]["name"],
            "get_weather",
        )

        self.assertEqual(
            tool["function"]["description"],
            "Get the current weather.",
        )

        self.assertEqual(
            tool["function"]["parameters"]["type"],
            "object",
        )

        self.assertEqual(
            tool["function"]["parameters"]["required"],
            ["location"],
        )

    def test_request_tool_call_message(self):
        request = ChatRequest(
            messages=[
                Message(
                    role="assistant",
                    content="",
                    tool_calls=[
                        ToolCall(
                            id="call_123",
                            name="get_weather",
                            arguments={
                                "location": "Lagos",
                            },
                        ),
                    ],
                ),
                Message(
                    role="tool",
                    content='{"temperature": 28}',
                    tool_call_id="call_123",
                ),
            ],
        )

        payload = OpenAISerializer.request(
            request,
            "gpt-4.1-mini",
        )

        assistant_message = payload["messages"][0]

        self.assertEqual(
            assistant_message["role"],
            "assistant",
        )

        self.assertEqual(
            assistant_message["tool_calls"][0]["id"],
            "call_123",
        )

        self.assertEqual(
            assistant_message["tool_calls"][0]["type"],
            "function",
        )

        self.assertEqual(
            assistant_message["tool_calls"][0]["function"]["name"],
            "get_weather",
        )

        self.assertEqual(
            assistant_message["tool_calls"][0]["function"]["arguments"],
            '{"location": "Lagos"}',
        )

        tool_message = payload["messages"][1]

        self.assertEqual(
            tool_message["role"],
            "tool",
        )

        self.assertEqual(
            tool_message["tool_call_id"],
            "call_123",
        )

        self.assertEqual(
            tool_message["content"],
            '{"temperature": 28}',
        )

    def test_response(self):
        payload = {
            "model": "gpt-4.1-mini",
            "choices": [
                {
                    "message": {
                        "content": "Hello back!",
                    },
                },
            ],
            "usage": {
                "prompt_tokens": 10,
            },
        }

        response = OpenAISerializer.response(
            payload,
        )

        self.assertEqual(
            response.content,
            "Hello back!",
        )

        self.assertEqual(
            response.model,
            "gpt-4.1-mini",
        )

        self.assertEqual(
            response.usage["prompt_tokens"],
            10,
        )

    def test_response_tool_call(self):
        payload = {
            "model": "gpt-4.1-mini",
            "choices": [
                {
                    "message": {
                        "content": None,
                        "tool_calls": [
                            {
                                "id": "call_123",
                                "type": "function",
                                "function": {
                                    "name": "get_weather",
                                    "arguments": (
                                        '{"location":"Lagos"}'
                                    ),
                                },
                            },
                        ],
                    },
                },
            ],
            "usage": {
                "prompt_tokens": 20,
            },
        }

        response = OpenAISerializer.response(
            payload,
        )

        self.assertEqual(
            len(response.tool_calls),
            1,
        )

        call = response.tool_calls[0]

        self.assertEqual(
            call.id,
            "call_123",
        )

        self.assertEqual(
            call.name,
            "get_weather",
        )

        self.assertEqual(
            call.arguments,
            {
                "location": "Lagos",
            },
        )

    def test_response_tool_call_with_object_arguments(self):
        payload = {
            "model": "gpt-4.1-mini",
            "choices": [
                {
                    "message": {
                        "content": None,
                        "tool_calls": [
                            {
                                "id": "call_456",
                                "type": "function",
                                "function": {
                                    "name": "add",
                                    "arguments": {
                                        "a": 2,
                                        "b": 3,
                                    },
                                },
                            },
                        ],
                    },
                },
            ],
        }

        response = OpenAISerializer.response(
            payload,
        )

        self.assertEqual(
            len(response.tool_calls),
            1,
        )

        call = response.tool_calls[0]

        self.assertEqual(
            call.id,
            "call_456",
        )

        self.assertEqual(
            call.name,
            "add",
        )

        self.assertEqual(
            call.arguments,
            {
                "a": 2,
                "b": 3,
            },
        )

    def test_invalid_response(self):
        with self.assertRaises(
            ProviderResponseError
        ):
            OpenAISerializer.response({})

    def test_invalid_tool_call_arguments(self):
        payload = {
            "model": "gpt-4.1-mini",
            "choices": [
                {
                    "message": {
                        "content": None,
                        "tool_calls": [
                            {
                                "id": "call_bad",
                                "type": "function",
                                "function": {
                                    "name": "add",
                                    "arguments": (
                                        '{"a": 2,'
                                    ),
                                },
                            },
                        ],
                    },
                },
            ],
        }

        with self.assertRaises(
            ProviderResponseError
        ):
            OpenAISerializer.response(payload)


if __name__ == "__main__":
    unittest.main()
