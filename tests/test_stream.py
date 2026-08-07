"""Tests for streaming models."""

import unittest

from app.providers.stream import ChatChunk


class ChatChunkTests(unittest.TestCase):
    """Tests for ChatChunk."""

    def test_defaults(self):
        chunk = ChatChunk("Hello")

        self.assertEqual(chunk.content, "Hello")
        self.assertFalse(chunk.finished)

    def test_finished_chunk(self):
        chunk = ChatChunk(
            content="Done",
            finished=True,
        )

        self.assertEqual(chunk.content, "Done")
        self.assertTrue(chunk.finished)


if __name__ == "__main__":
    unittest.main()
