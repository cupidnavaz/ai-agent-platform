"""Prompt builder tests."""

import unittest

from app.memory import ConversationMemory
from app.prompts import PromptBuilder


class TestPromptBuilder(unittest.TestCase):

    def test_prompt_build(self):

        memory = ConversationMemory()

        memory.add(
            role="user",
            content="Hello",
        )

        builder = PromptBuilder()

        prompt = builder.build(
            memory,
            "How are you?",
        )

        self.assertEqual(
            prompt[0]["role"],
            "system",
        )

        self.assertEqual(
            prompt[-1]["content"],
            "How are you?",
        )


if __name__ == "__main__":
    unittest.main()
