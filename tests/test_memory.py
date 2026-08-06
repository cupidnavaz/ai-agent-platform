"""Conversation memory tests."""

import unittest

from app.memory import ConversationMemory


class TestConversationMemory(unittest.TestCase):

    def test_add_message(self):

        memory = ConversationMemory()

        memory.add(
            role="user",
            content="Hello",
        )

        self.assertEqual(
            len(memory.history()),
            1,
        )

        self.assertEqual(
            memory.history()[0]["content"],
            "Hello",
        )

    def test_clear(self):

        memory = ConversationMemory()

        memory.add(
            role="user",
            content="Hello",
        )

        memory.clear()

        self.assertEqual(
            len(memory.history()),
            0,
        )


if __name__ == "__main__":
    unittest.main()
