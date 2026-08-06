"""Prompt builder."""

from app.memory import ConversationMemory


class PromptBuilder:
    """Build prompts for providers."""

    def __init__(self, system_prompt: str = "You are a helpful AI assistant.") -> None:
        self.system_prompt = system_prompt

    def build(self, memory: ConversationMemory, message: str) -> list[dict[str, str]]:
        messages = [
            {
                "role": "system",
                "content": self.system_prompt,
            }
        ]

        messages.extend(memory.history())

        messages.append(
            {
                "role": "user",
                "content": message,
            }
        )

        return messages
