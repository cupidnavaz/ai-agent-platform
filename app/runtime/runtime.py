"""AI Agent Runtime."""

from __future__ import annotations

from app.container import Container
from app.sessions import manager as session_manager


class Runtime:
    """Central runtime for managing assistant sessions."""

    def __init__(
        self,
        container: Container,
    ) -> None:
        """Initialize the runtime."""

        self.container = container
        self._assistants: dict[str, object] = {}

    def create_session(self) -> str:
        """Create a new runtime session."""

        session_id = session_manager.create()

        self._assistants[session_id] = (
            self.container.assistant()
        )

        return session_id

    def chat(
        self,
        session_id: str,
        message: str,
    ) -> str:
        """Send a message to an assistant session."""

        assistant = self._get_assistant(
            session_id
        )

        return assistant.chat(message)

    def history(
        self,
        session_id: str,
    ):
        """Return chat history for a session."""

        assistant = self._get_assistant(
            session_id
        )

        return assistant.history()

    def clear_history(
        self,
        session_id: str,
    ) -> None:
        """Clear chat history for a session."""

        assistant = self._get_assistant(
            session_id
        )

        assistant.clear()

    def delete_session(
        self,
        session_id: str,
    ) -> bool:
        """Delete a runtime session."""

        self._assistants.pop(
            session_id,
            None,
        )

        return session_manager.delete(
            session_id
        )

    def _get_assistant(
        self,
        session_id: str,
    ):
        """Return the assistant for a session."""

        assistant = self._assistants.get(
            session_id
        )

        if assistant is None:
            raise ValueError(
                "Invalid session."
            )

        return assistant
