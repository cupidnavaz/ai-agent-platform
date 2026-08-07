"""Tests for the OpenAI provider."""

import unittest

from app.providers.openai import OpenAIProvider
from app.providers.openai_config import OpenAIConfig


class OpenAIProviderTests(unittest.TestCase):
    """OpenAI provider tests."""

    def setUp(self) -> None:
        self.config = OpenAIConfig(
            api_key="test-key",
            base_url="https://api.openai.com/v1",
            timeout=30.0,
            model="gpt-4.1-mini",
        )

    def test_name(self):
        provider = OpenAIProvider(self.config)

        self.assertEqual(
            provider.name,
            "openai",
        )

    def test_models(self):
        provider = OpenAIProvider(self.config)

        self.assertEqual(
            provider.models(),
            ["gpt-4.1-mini"],
        )

    def test_health_true(self):
        provider = OpenAIProvider(
            OpenAIConfig(
                api_key="abc123",
                base_url="https://api.openai.com/v1",
                timeout=30.0,
                model="gpt-4.1-mini",
            )
        )

        self.assertTrue(provider.health())

    def test_health_false(self):
        provider = OpenAIProvider(
            OpenAIConfig(
                api_key="",
                base_url="https://api.openai.com/v1",
                timeout=30.0,
                model="gpt-4.1-mini",
            )
        )

        self.assertFalse(provider.health())


if __name__ == "__main__":
    unittest.main()
