"""Tests for OpenAI configuration."""

import os
import unittest

from app.providers.openai_config import OpenAIConfig


class TestOpenAIConfig(unittest.TestCase):
    """Test OpenAI configuration."""

    def setUp(self) -> None:
        self._env = os.environ.copy()

    def tearDown(self) -> None:
        os.environ.clear()
        os.environ.update(self._env)

    def test_from_env_defaults(self):
        os.environ["OPENAI_API_KEY"] = "test-key"

        config = OpenAIConfig.from_env()

        self.assertEqual(config.api_key, "test-key")
        self.assertEqual(
            config.base_url,
            "https://api.openai.com/v1",
        )
        self.assertEqual(
            config.model,
            "gpt-4.1-mini",
        )
        self.assertEqual(
            config.timeout,
            30.0,
        )

    def test_from_env_custom_values(self):
        os.environ["OPENAI_API_KEY"] = "abc123"
        os.environ["OPENAI_MODEL"] = "gpt-4.1"
        os.environ["OPENAI_BASE_URL"] = "https://example.com/v1"
        os.environ["OPENAI_TIMEOUT"] = "60"

        config = OpenAIConfig.from_env()

        self.assertEqual(config.api_key, "abc123")
        self.assertEqual(
            config.model,
            "gpt-4.1",
        )
        self.assertEqual(
            config.base_url,
            "https://example.com/v1",
        )
        self.assertEqual(
            config.timeout,
            60.0,
        )

    def test_missing_api_key(self):
        os.environ.pop(
            "OPENAI_API_KEY",
            None,
        )

        with self.assertRaises(ValueError):
            OpenAIConfig.from_env()


if __name__ == "__main__":
    unittest.main()
