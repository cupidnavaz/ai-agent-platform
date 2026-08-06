"""Provider tests."""

import unittest

from app.providers.mock import MockProvider
from app.providers.models import (
    ChatRequest,
    Message,
)


class TestMockProvider(unittest.TestCase):

    def test_chat(self):

        provider = MockProvider()

        request = ChatRequest(
            messages=[
                Message(
                    role="user",
                    content="Hello",
                )
            ]
        )

        response = provider.chat(request)

        self.assertEqual(
            response.content,
            "Mock response: Hello",
        )


if __name__ == "__main__":
    unittest.main()
