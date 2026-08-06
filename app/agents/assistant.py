"""AI Assistant."""

import app.commands.defaults

from app.commands import router
from app.memory import ConversationMemory
from app.prompts import PromptBuilder
from app.providers.provider import Provider


class Assistant:
    """High-level AI assistant."""

    def __init__(
        self,
        provider: Provider,
        system_prompt: str = "You are a helpful AI assistant.",
    ) -> None:
        self.provider = provider
        self.memory = ConversationMemory()
        self.prompt_builder = PromptBuilder(system_prompt)

    def chat(self, message: str) -> str:

        self.memory.add(
            role="user",
            content=message,
        )

        command_result = router.execute(message)

        if command_result is not None:

            self.memory.add(
                role="assistant",
                content=command_result,
                provider="command",
            )

            return command_result

        messages = self.prompt_builder.build(
            self.memory,
            message,
        )

        response = self.provider.chat(messages)

        self.memory.add(
            role="assistant",
            content=response,
            provider=self.provider.name,
        )

        return response

    def history(self):
        return self.memory.history()

    def clear(self):
        self.memory.clear()
