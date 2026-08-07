"""Tests for provider serializers."""

import unittest

from app.providers.errors import ProviderResponseError
from app.providers.models import (
    ChatRequest,
    ChatResponse,
    Message,
)
from app.providers.serializers import OpenAISerializer


class OpenAISerializerTests(unittest.TestCase):
    """Tests for the OpenAI serializer."""

    def test_request_defaults(self):
        request = ChatRequest(
            messages=[
                Message(
                    role="user",
                    content="Hello",
                )
            ]
        )

        payload = OpenAISerializer.request(
            request,
            "gpt-4.1-mini",
        )

        self.assertEqual(
            payload["model"],
            "gpt-4.1-mini",
        )

        self.assertEqual(
            payload["temperature"],
            0.7,
        )

        self.assertEqual(
            payload["messages"],
            [
                {
                    "role": "user",
                    "content": "Hello",
                }
            ],
        )

        self.assertNotIn(
            "max_tokens",
            payload,
        )

    def test_request_custom_model(self):
        request = ChatRequest(
            model="gpt-5",
            messages=[
                Message(
                    role="user",
                    content="Hi",
                )
            ],
        )

        payload = OpenAISerializer.request(
            request,
            "gpt-4.1-mini",
        )

        self.assertEqual(
            payload["model"],
            "gpt-5",
        )

    def test_request_max_tokens(self):
        request = ChatRequest(
            messages=[
                Message(
                    role="user",
                    content="Hello",
                )
            ],
            max_tokens=200,
        )

        payload = OpenAISerializer.request(
            request,
            "gpt-4.1-mini",
        )

        self.assertEqual(
            payload["max_tokens"],
            200,
        )

    def test_response(self):
        payload = {
            "model": "gpt-4.1-mini",
            "choices": [
                {
                    "message": {
                        "content": "Hello back!"
                    }
                }
            ],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 5,
            },
        }

        response = OpenAISerializer.response(
            payload
        )

        self.assertIsInstance(
            response,
            ChatResponse,
        )

        self.assertEqual(
            response.content,
            "Hello back!",
        )

        self.assertEqual(
            response.model,
            "gpt-4.1-mini",
        )

        self.assertEqual(
            response.usage["prompt_tokens"],
            10,
        )

    def test_invalid_response(self):
        with self.assertRaises(
            ProviderResponseError
        ):
            OpenAISerializer.response({})


if __name__ == "__main__":
    unittest.main()
