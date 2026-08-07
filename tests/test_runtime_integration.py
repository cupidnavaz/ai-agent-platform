"""Runtime integration tests."""

import unittest

from app.container import Container
from app.providers.mock import MockProvider
from app.runtime.runtime import Runtime


class TestRuntimeIntegration(unittest.TestCase):
    """End-to-end runtime tests."""

    def setUp(self):
        self.provider = MockProvider()
        self.container = Container(self.provider)
        self.runtime = Runtime(self.container)

    def test_chat_flow(self):
        """Runtime should create a session and chat."""

        session = self.runtime.create_session()

        response = self.runtime.chat(
            session,
            "Hello",
        )

        self.assertEqual(
            response,
            "Mock response: Hello",
        )

    def test_history(self):
        """Conversation history should be stored."""

        session = self.runtime.create_session()

        self.runtime.chat(
            session,
            "Hello",
        )

        history = self.runtime.history(session)

        self.assertEqual(
            len(history),
            2,
        )

        self.assertEqual(
            history[0]["role"],
            "user",
        )

        self.assertEqual(
            history[1]["role"],
            "assistant",
        )

    def test_invalid_session(self):
        """Invalid session should raise an error."""

        with self.assertRaises(ValueError):
            self.runtime.chat(
                "invalid",
                "Hello",
            )


if __name__ == "__main__":
    unittest.main()
