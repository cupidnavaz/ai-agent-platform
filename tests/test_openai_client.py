"""Tests for the OpenAI client."""

import unittest
from unittest.mock import MagicMock

from app.providers.openai_client import OpenAIClient
from app.providers.openai_config import OpenAIConfig


class TestOpenAIClient(unittest.TestCase):
    """Test OpenAIClient."""

    def setUp(self) -> None:
        self.config = OpenAIConfig(
            api_key="test-key",
            base_url="https://example.com/v1",
            timeout=30.0,
            model="gpt-4.1-mini",
        )

    def test_headers(self):
        client = OpenAIClient(self.config)

        self.assertEqual(
            client.headers["Authorization"],
            "Bearer test-key",
        )

        self.assertEqual(
            client.headers["Content-Type"],
            "application/json",
        )

    def test_health(self):
        client = OpenAIClient(self.config)

        self.assertTrue(client.health())

    def test_post_uses_transport(self):
        client = OpenAIClient(self.config)

        client.transport = MagicMock()

        client.transport.post.return_value = "response"

        result = client.post(
            "chat/completions",
            {"model": "gpt"},
        )

        self.assertEqual(result, "response")

        client.transport.post.assert_called_once_with(
            url="https://example.com/v1/chat/completions",
            headers=client.headers,
            payload={"model": "gpt"},
        )


if __name__ == "__main__":
    unittest.main()
