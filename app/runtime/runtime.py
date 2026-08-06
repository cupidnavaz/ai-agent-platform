"""AI Agent Runtime."""

from app.container import Container
from app.sessions import manager as session_manager


class Runtime:
    """Central runtime."""

    def __init__(self, container: Container):
        self.container = container
        self._assistants = {}

    def create_session(self) -> str:
        session_id = session_manager.create()

        self._assistants[session_id] = (
            self.container.assistant()
        )

        return session_id

    def chat(
        self,
        session_id: str,
        message: str,
    ):

        assistant = self._assistants.get(session_id)

        if assistant is None:
            raise ValueError("Invalid session.")

        return assistant.chat(message)

    def history(self, session_id: str):
        assistant = self._assistants.get(session_id)

        if assistant is None:
            raise ValueError("Invalid session.")

        return assistant.history()

    def delete_session(self, session_id: str):
        self._assistants.pop(session_id, None)
        return session_manager.delete(session_id)
