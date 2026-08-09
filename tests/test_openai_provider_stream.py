"""Tests for OpenAI provider streaming."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock

from app.providers.models import ChatRequest, Message
from app.providers.openai import OpenAIProvider
from app.providers.openai_config import OpenAIConfig


class OpenAIProviderStreamTests(unittest.TestCase):
    """OpenAI provider streaming tests."""

    def setUp(self):
        config = OpenAIConfig(
            api_key="test-key",
            base_url="https://api.openai.com/v1",
            timeout=30.0,
            model="gpt-4.1-mini",
        )

        self.client = MagicMock()
        self.provider = OpenAIProvider(
            config,
            client=self.client,
        )

    def test_stream_chat(self):
        self.client.stream.return_value = iter(
            [
                {
                    "choices": [
                        {
                            "delta": {
                                "content": "Hello",
                            },
                            "finish_reason": None,
                        }
                    ]
                },
                {
                    "choices": [
                        {
                            "delta": {
                                "content": " world",
                            },
                            "finish_reason": None,
                        }
                    ]
                },
                {
                    "choices": [
                        {
                            "delta": {},
                            "finish_reason": "stop",
                        }
                    ]
                },
            ]
        )

        request = ChatRequest(
            messages=[
                Message(
                    role="user",
                    content="Say hello.",
                )
            ],
            temperature=0.0,
        )

        chunks = list(
            self.provider.stream_chat(request)
        )

        self.assertEqual(
            [chunk.content for chunk in chunks],
            ["Hello", " world", ""],
        )

        self.assertTrue(
            chunks[-1].finished,
        )

        self.client.stream.assert_called_once()

        _, payload = self.client.stream.call_args.args

        self.assertEqual(
            payload["model"],
            "gpt-4.1-mini",
        )

        self.assertTrue(
            payload["stream"],
        )


if __name__ == "__main__":
    unittest.main()
