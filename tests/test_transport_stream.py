"""Tests for HTTPTransport.stream()."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from app.providers.transport import HTTPTransport


class HTTPTransportStreamTests(unittest.TestCase):
    """Tests for HTTPTransport.stream()."""

    def setUp(self):
        self.transport = HTTPTransport()

    @patch("app.providers.transport.urlopen")
    def test_stream(self, mock_urlopen):
        response = MagicMock()

        response.__enter__.return_value = response
        response.__iter__.return_value = iter(
            [
                b"data: first\n",
                b"\n",
                b"data: second\n",
                b"data: [DONE]\n",
            ]
        )

        mock_urlopen.return_value = response

        chunks = list(
            self.transport.stream(
                url="https://example.com",
                headers={},
                payload={},
            )
        )

        self.assertEqual(
            chunks,
            [
                "data: first",
                "data: second",
                "data: [DONE]",
            ],
        )


if __name__ == "__main__":
    unittest.main()
