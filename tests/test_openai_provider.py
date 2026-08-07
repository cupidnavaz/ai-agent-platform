"""Tests for the OpenAI provider."""

import unittest

from app.providers.openai import OpenAIProvider


class OpenAIProviderTests(unittest.TestCase):
    """OpenAI provider tests."""

    def test_name(self):
        provider = OpenAIProvider("test-key")

        self.assertEqual(
            provider.name,
            "openai",
        )

    def test_models(self):
        provider = OpenAIProvider("test-key")

        self.assertEqual(
            provider.models(),
            ["gpt-4.1-mini"],
        )

    def test_health_true(self):
        provider = OpenAIProvider("abc123")

        self.assertTrue(
            provider.health(),
        )

    def test_health_false(self):
        provider = OpenAIProvider("")

        self.assertFalse(
            provider.health(),
        )


if __name__ == "__main__":
    unittest.main()
