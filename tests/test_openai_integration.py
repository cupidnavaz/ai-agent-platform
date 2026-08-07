"""Integration tests for the OpenAI provider."""

from __future__ import annotations

import os
import unittest

from app.providers.models import (
    ChatRequest,
    Message,
)
from app.providers.openai import OpenAIProvider
from app.providers.openai_config import OpenAIConfig


RUN_INTEGRATION = (
    os.getenv("RUN_OPENAI_INTEGRATION_TESTS") == "1"
)


@unittest.skipUnless(
    RUN_INTEGRATION,
    "Integration tests are disabled.",
)
class OpenAIIntegrationTests(unittest.TestCase):
    """Real OpenAI integration tests."""

    def setUp(self) -> None:
        self.config = OpenAIConfig.from_env()
        self.provider = OpenAIProvider(self.config)

    def test_chat(self):
        request = ChatRequest(
            messages=[
                Message(
                    role="user",
                    content="Reply with exactly: Hello from OpenAI",
                )
            ],
            temperature=0.0,
        )

        response = self.provider.chat(request)

        self.assertIsInstance(response.content, str)
        self.assertGreater(
            len(response.content.strip()),
            0,
        )

        self.assertEqual(
            response.model,
            self.config.model,
        )


if __name__ == "__main__":
    unittest.main()
