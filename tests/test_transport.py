"""Tests for HTTP transport."""

import unittest
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError, URLError

from app.providers.errors import (
    ProviderAuthenticationError,
    ProviderConnectionError,
    ProviderRateLimitError,
    ProviderResponseError,
    ProviderTimeoutError,
)
from app.providers.transport import HTTPResponse, HTTPTransport


class TestHTTPTransport(unittest.TestCase):
    """Test HTTPTransport."""

    def setUp(self) -> None:
        self.transport = HTTPTransport()
        self.url = "https://example.com"
        self.headers = {}
        self.payload = {}

    @patch("app.providers.transport.urlopen")
    def test_success(self, mock_urlopen):
        response = MagicMock()
        response.status = 200
        response.read.return_value = b'{"message":"ok"}'

        mock_urlopen.return_value.__enter__.return_value = response

        result = self.transport.post(
            self.url,
            self.headers,
            self.payload,
        )

        self.assertIsInstance(result, HTTPResponse)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.body, {"message": "ok"})

    @patch("app.providers.transport.urlopen")
    def test_authentication_error(self, mock_urlopen):
        mock_urlopen.side_effect = HTTPError(
            self.url,
            401,
            "Unauthorized",
            {},
            None,
        )

        with self.assertRaises(ProviderAuthenticationError):
            self.transport.post(
                self.url,
                self.headers,
                self.payload,
            )

    @patch("app.providers.transport.urlopen")
    def test_rate_limit_error(self, mock_urlopen):
        mock_urlopen.side_effect = HTTPError(
            self.url,
            429,
            "Too Many Requests",
            {},
            None,
        )

        with self.assertRaises(ProviderRateLimitError):
            self.transport.post(
                self.url,
                self.headers,
                self.payload,
            )

    @patch("app.providers.transport.urlopen")
    def test_http_error(self, mock_urlopen):
        mock_urlopen.side_effect = HTTPError(
            self.url,
            500,
            "Internal Server Error",
            {},
            None,
        )

        with self.assertRaises(ProviderResponseError):
            self.transport.post(
                self.url,
                self.headers,
                self.payload,
            )

    @patch("app.providers.transport.urlopen")
    def test_connection_error(self, mock_urlopen):
        mock_urlopen.side_effect = URLError("offline")

        with self.assertRaises(ProviderConnectionError):
            self.transport.post(
                self.url,
                self.headers,
                self.payload,
            )

    @patch("app.providers.transport.urlopen")
    def test_timeout(self, mock_urlopen):
        mock_urlopen.side_effect = TimeoutError()

        with self.assertRaises(ProviderTimeoutError):
            self.transport.post(
                self.url,
                self.headers,
                self.payload,
            )


if __name__ == "__main__":
    unittest.main()
