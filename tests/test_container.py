"""Container tests."""

import unittest

from app.container import Container
from app.providers.mock import MockProvider


class TestContainer(unittest.TestCase):

    def test_container_creates_assistant(self):

        provider = MockProvider()

        container = Container(provider)

        assistant = container.assistant()

        self.assertIsNotNone(assistant)
        self.assertEqual(
            assistant.provider.name,
            "mock",
        )


if __name__ == "__main__":
    unittest.main()
