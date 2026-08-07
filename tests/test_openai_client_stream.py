"""Tests for OpenAIClient.stream()."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock

from app.providers.openai_client import OpenAIClient
from app.providers.openai_config import OpenAIConfig


class OpenAIClientStreamTests(unittest.TestCase):
    """Tests for OpenAIClient.stream()."""

    def setUp(self):
        config = OpenAIConfig(
            api_key="test-key",
            base_url="https://api.openai.com/v1",
            timeout=30.0,
            model="gpt-4.1-mini",
        )

        self.client = OpenAIClient(config)
        self.client.transport = MagicMock()

    def test_stream(self):
        self.client.transport.stream.return_value = iter(
            [
                'data: {"id":"1"}',
                'data: {"id":"2"}',
                "data: [DONE]",
            ]
        )

        events = list(
            self.client.stream(
                "chat/completions",
                {},
            )
        )

        self.assertEqual(
            events,
            [
                {"id": "1"},
                {"id": "2"},
            ],
        )


if __name__ == "__main__":
    unittest.main()
