"""AI Assistant."""

import app.commands.defaults

from app.commands import router
from app.memory import ConversationMemory
from app.prompts import PromptBuilder

from app.providers.provider import Provider
from app.providers.models import (
    Message,
    ChatRequest,
)


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

    def chat(
        self,
        message: str,
    ) -> str:

        command_result = router.execute(message)

        if command_result is not None:

            self.memory.add(
                role="user",
                content=message,
            )

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

        request = ChatRequest(
            messages=[
                Message(
                    role=item["role"],
                    content=item["content"],
                )
                for item in messages
            ]
        )

        response = self.provider.chat(request)

        self.memory.add(
            role="user",
            content=message,
        )

        self.memory.add(
            role="assistant",
            content=response.content,
            provider=self.provider.name,
        )

        return response.content

    def history(self):
        return self.memory.history()

    def clear(self):
        self.memory.clear()
