"""AI Assistant."""

import app.commands.defaults

from app.commands import router
from app.memory import ConversationMemory
from app.prompts import PromptBuilder
from app.providers.base import BaseProvider
from app.providers.models import (
    ChatRequest,
    Message,
)


class Assistant:
    """High-level AI assistant."""

    def __init__(
        self,
        provider: BaseProvider,
        system_prompt: str = "You are a helpful AI assistant.",
    ) -> None:
        self.provider = provider
        self.memory = ConversationMemory()
        self.prompt_builder = PromptBuilder(system_prompt)

    def chat(
        self,
        message: str,
    ) -> str:
        """Process a chat message."""

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
        """Return conversation history."""
        return self.memory.history()

    def clear(self):
        """Clear conversation history."""
        self.memory.clear()
