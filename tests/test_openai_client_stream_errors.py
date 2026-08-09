"""Tests for OpenAI streaming client errors."""

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


class OpenAIClientStreamErrorTests(unittest.TestCase):
    """OpenAI streaming error tests."""

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
        body: dict | None = None,
    ) -> HTTPResponse:
        return HTTPResponse(
            status_code=status_code,
            body=body or {},
        )

    def test_stream_authentication_error(self):
        self.client.transport.stream.side_effect = (
            ProviderAuthenticationError(
                "Authentication failed."
            )
        )

        with self.assertRaises(
            ProviderAuthenticationError
        ):
            list(
                self.client.stream(
                    "chat/completions",
                    {"model": "gpt-4.1-mini"},
                )
            )

    def test_stream_rate_limit_error(self):
        self.client.transport.stream.side_effect = (
            ProviderRateLimitError(
                "Rate limit exceeded."
            )
        )

        with self.assertRaises(
            ProviderRateLimitError
        ):
            list(
                self.client.stream(
                    "chat/completions",
                    {"model": "gpt-4.1-mini"},
                )
            )

    def test_stream_timeout_error(self):
        self.client.transport.stream.side_effect = (
            ProviderTimeoutError(
                "Request timed out."
            )
        )

        with self.assertRaises(
            ProviderTimeoutError
        ):
            list(
                self.client.stream(
                    "chat/completions",
                    {"model": "gpt-4.1-mini"},
                )
            )

    def test_stream_connection_error(self):
        self.client.transport.stream.side_effect = (
            ProviderConnectionError(
                "Connection failed."
            )
        )

        with self.assertRaises(
            ProviderConnectionError
        ):
            list(
                self.client.stream(
                    "chat/completions",
                    {"model": "gpt-4.1-mini"},
                )
            )

    def test_stream_response_error(self):
        self.client.transport.stream.side_effect = (
            ProviderResponseError(
                "Invalid response."
            )
        )

        with self.assertRaises(
            ProviderResponseError
        ):
            list(
                self.client.stream(
                    "chat/completions",
                    {"model": "gpt-4.1-mini"},
                )
            )

    def test_stream_invalid_json(self):
        self.client.transport.stream.return_value = iter(
            [
                "data: {invalid-json}",
            ]
        )

        with self.assertRaises(
            ProviderResponseError
        ):
            list(
                self.client.stream(
                    "chat/completions",
                    {"model": "gpt-4.1-mini"},
                )
            )


if __name__ == "__main__":
    unittest.main()
