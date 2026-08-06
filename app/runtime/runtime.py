"""AI Agent Runtime."""

from app.agents.assistant import Assistant
from app.providers.provider import Provider
from app.sessions import manager as session_manager


class Runtime:
    """Central runtime for AI agents."""

    def __init__(self, provider: Provider):
        self.provider = provider

        self._assistants: dict[str, Assistant] = {}

    def create_session(self) -> str:
        session_id = session_manager.create()

        self._assistants[session_id] = Assistant(
            provider=self.provider,
        )

        return session_id

    def chat(
        self,
        session_id: str,
        message: str,
    ) -> str:

        assistant = self._assistants.get(session_id)

        if assistant is None:
            raise ValueError("Invalid session.")

        return assistant.chat(message)

    def history(self, session_id: str):

        assistant = self._assistants.get(session_id)

        if assistant is None:
            raise ValueError("Invalid session.")

        return assistant.history()

    def delete_session(
        self,
        session_id: str,
    ) -> bool:

        self._assistants.pop(session_id, None)

        return session_manager.delete(session_id)
