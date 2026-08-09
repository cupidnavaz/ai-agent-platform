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

        history = self.runtime.history(
            session
        )

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

    def test_sessions_have_isolated_history(self):
        """Each runtime session should have separate history."""

        first_session = self.runtime.create_session()
        second_session = self.runtime.create_session()

        self.runtime.chat(
            first_session,
            "First",
        )

        self.runtime.chat(
            second_session,
            "Second",
        )

        first_history = self.runtime.history(
            first_session
        )

        second_history = self.runtime.history(
            second_session
        )

        self.assertEqual(
            len(first_history),
            2,
        )

        self.assertEqual(
            len(second_history),
            2,
        )

        self.assertEqual(
            first_history[0]["content"],
            "First",
        )

        self.assertEqual(
            second_history[0]["content"],
            "Second",
        )

    def test_clear_history(self):
        """Runtime should clear a session's history."""

        session = self.runtime.create_session()

        self.runtime.chat(
            session,
            "Hello",
        )

        self.runtime.clear_history(
            session
        )

        self.assertEqual(
            self.runtime.history(session),
            [],
        )

    def test_delete_session(self):
        """Runtime should delete a session."""

        session = self.runtime.create_session()

        self.assertTrue(
            self.runtime.delete_session(
                session
            )
        )

        with self.assertRaises(ValueError):
            self.runtime.chat(
                session,
                "Hello",
            )

    def test_invalid_session_chat(self):
        """Invalid chat sessions should raise ValueError."""

        with self.assertRaises(ValueError):
            self.runtime.chat(
                "invalid",
                "Hello",
            )

    def test_invalid_session_history(self):
        """Invalid history sessions should raise ValueError."""

        with self.assertRaises(ValueError):
            self.runtime.history(
                "invalid"
            )

    def test_invalid_session_clear_history(self):
        """Invalid history clears should raise ValueError."""

        with self.assertRaises(ValueError):
            self.runtime.clear_history(
                "invalid"
            )


if __name__ == "__main__":
    unittest.main()
