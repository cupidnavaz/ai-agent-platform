"""Conversation session manager."""

from uuid import uuid4

from app.memory import ConversationMemory


class SessionManager:
    """Manages multiple conversation sessions."""

    def __init__(self):
        self._sessions: dict[str, ConversationMemory] = {}

    def create(self) -> str:
        session_id = str(uuid4())

        self._sessions[session_id] = ConversationMemory()

        return session_id

    def get(self, session_id: str) -> ConversationMemory | None:
        return self._sessions.get(session_id)

    def delete(self, session_id: str) -> bool:
        return self._sessions.pop(session_id, None) is not None

    def list(self):
        return sorted(self._sessions.keys())


manager = SessionManager()
