"""Tests for OpenAI client error handling."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock

from app.providers.errors import (
    ProviderAuthenticationError,
    ProviderConnectionError,
    ProviderRateLimitError,
    ProviderResponseError,
    ProviderTimeoutError,
)
from app.providers.openai_client import OpenAIClient
from app.providers.openai_config import OpenAIConfig
from app.providers.transport import HTTPResponse


class OpenAIClientErrorTests(unittest.TestCase):
    """OpenAI client HTTP error tests."""

    def setUp(self):
        config = OpenAIConfig(
            api_key="test-key",
            base_url="https://api.openai.com/v1",
            timeout=30.0,
            model="gpt-4.1-mini",
        )

        self.client = OpenAIClient(config)
        self.client.transport = MagicMock()

    def _response(
        self,
        status_code: int,
        body: dict | str | None = None,
    ) -> HTTPResponse:
        return HTTPResponse(
            status_code=status_code,
            body=body if body is not None else {},
        )

    def test_401_raises_authentication_error(self):
        self.client.transport.post.return_value = self._response(
            401,
            {"error": {"message": "Invalid API key."}},
        )

        with self.assertRaises(
            ProviderAuthenticationError,
        ):
            self.client.post(
                "chat/completions",
                {"model": "gpt-4.1-mini"},
            )

    def test_403_raises_authentication_error(self):
        self.client.transport.post.return_value = self._response(
            403,
            {"error": {"message": "Forbidden."}},
        )

        with self.assertRaises(
            ProviderAuthenticationError,
        ):
            self.client.post(
                "chat/completions",
                {"model": "gpt-4.1-mini"},
            )

    def test_429_raises_rate_limit_error(self):
        self.client.transport.post.return_value = self._response(
            429,
            {"error": {"message": "Rate limit exceeded."}},
        )

        with self.assertRaises(
            ProviderRateLimitError,
        ):
            self.client.post(
                "chat/completions",
                {"model": "gpt-4.1-mini"},
            )

    def test_408_raises_timeout_error(self):
        self.client.transport.post.return_value = self._response(
            408,
            {"error": {"message": "Request timeout."}},
        )

        with self.assertRaises(
            ProviderTimeoutError,
        ):
            self.client.post(
                "chat/completions",
                {"model": "gpt-4.1-mini"},
            )

    def test_5xx_raises_connection_error(self):
        self.client.transport.post.return_value = self._response(
            500,
            {"error": {"message": "Server error."}},
        )

        with self.assertRaises(
            ProviderConnectionError,
        ):
            self.client.post(
                "chat/completions",
                {"model": "gpt-4.1-mini"},
            )

    def test_other_4xx_raises_response_error(self):
        self.client.transport.post.return_value = self._response(
            400,
            {"error": {"message": "Bad request."}},
        )

        with self.assertRaises(
            ProviderResponseError,
        ):
            self.client.post(
                "chat/completions",
                {"model": "gpt-4.1-mini"},
            )


if __name__ == "__main__":
    unittest.main()
