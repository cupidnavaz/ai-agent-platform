"""Tests for OpenAI provider tool calling."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock

from app.providers.models import (
    ChatRequest,
    Message,
    ToolDefinition,
)
from app.providers.openai import OpenAIProvider
from app.providers.openai_config import OpenAIConfig
from app.providers.tools import ToolRegistry


class OpenAIProviderToolTests(unittest.TestCase):
    """OpenAI provider tool-calling tests."""

    def setUp(self):
        config = OpenAIConfig(
            api_key="test-key",
            base_url="https://api.openai.com/v1",
            timeout=30.0,
            model="gpt-4.1-mini",
        )

        self.client = MagicMock()

        self.registry = ToolRegistry()

        self.provider = OpenAIProvider(
            config,
            client=self.client,
            tool_registry=self.registry,
        )

    def test_tool_call_executes_and_returns_final_response(self):
        """Provider should execute a requested tool and continue."""

        self.registry.register(
            ToolDefinition(
                name="add",
                description="Add two numbers.",
            ),
            lambda a, b: a + b,
        )

        first_response = MagicMock()

        first_response.body = {
            "model": "gpt-4.1-mini",
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [
                            {
                                "id": "call_123",
                                "type": "function",
                                "function": {
                                    "name": "add",
                                    "arguments": (
                                        '{"a": 2, "b": 3}'
                                    ),
                                },
                            }
                        ],
                    },
                    "finish_reason": "tool_calls",
                }
            ],
            "usage": {},
        }

        second_response = MagicMock()

        second_response.body = {
            "model": "gpt-4.1-mini",
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "The answer is 5.",
                    },
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 5,
            },
        }

        self.client.post.side_effect = [
            first_response,
            second_response,
        ]

        request = ChatRequest(
            messages=[
                Message(
                    role="user",
                    content="What is 2 + 3?",
                )
            ],
            temperature=0.0,
        )

        response = self.provider.chat(request)

        self.assertEqual(
            response.content,
            "The answer is 5.",
        )

        self.assertEqual(
            self.client.post.call_count,
            2,
        )

        first_call_payload = (
            self.client.post.call_args_list[0]
            .args[1]
        )

        self.assertEqual(
            first_call_payload["model"],
            "gpt-4.1-mini",
        )

        self.assertIn(
            "tools",
            first_call_payload,
        )

        second_call_payload = (
            self.client.post.call_args_list[1]
            .args[1]
        )

        messages = second_call_payload["messages"]

        self.assertEqual(
            messages[-1]["role"],
            "tool",
        )

        self.assertEqual(
            messages[-1]["tool_call_id"],
            "call_123",
        )

        self.assertEqual(
            messages[-1]["content"],
            "5",
        )


if __name__ == "__main__":
    unittest.main()
