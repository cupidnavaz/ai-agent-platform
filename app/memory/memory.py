"""Conversation memory."""

from datetime import UTC, datetime


class ConversationMemory:
    """Stores conversation history."""

    def __init__(self) -> None:
        self._history: list[dict] = []

    def add(
        self,
        role: str,
        content: str,
        provider: str | None = None,
    ) -> None:
        """Add a message to the conversation history."""

        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now(UTC).isoformat(),
        }

        if provider is not None:
            message["provider"] = provider

        self._history.append(message)

    def history(self) -> list[dict]:
        """Return the conversation history."""
        return self._history.copy()

    def clear(self) -> None:
        """Clear the conversation history."""
        self._history.clear()

    def last(self) -> dict | None:
        """Return the last message, if any."""
        if not self._history:
            return None

        return self._history[-1]

    def __len__(self) -> int:
        """Return the number of stored messages."""
        return len(self._history)
