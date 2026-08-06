"""Conversation memory."""

from datetime import datetime
from uuid import uuid4


class ConversationMemory:
    """Stores conversation history."""

    def __init__(self):
        self._history = []

    def add(
        self,
        role: str,
        content: str,
        provider: str = "",
        metadata: dict | None = None,
    ):
        self._history.append(
            {
                "id": str(uuid4()),
                "timestamp": datetime.utcnow().isoformat(),
                "role": role,
                "content": content,
                "provider": provider,
                "metadata": metadata or {},
            }
        )

    def history(self):
        return list(self._history)

    def clear(self):
        self._history.clear()
