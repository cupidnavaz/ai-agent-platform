"""AI Assistant service."""

from app.memory import ConversationMemory
from app.providers import Provider


class Assistant:
    """Simple AI assistant."""

    def __init__(self, provider: Provider):
        self.provider = provider
        self.memory = ConversationMemory()

    def chat(self, message: str):
        self.memory.add("user", message)

        reply = self.provider.generate(message)

        self.memory.add("assistant", reply)

        return reply

    def history(self):
        return self.memory.history()

    def clear(self):
        self.memory.clear()
