"""AI Agent Runtime."""

from app.container import Container
from app.sessions import manager as session_manager
from app.storage import (
    SQLiteStorage,
    MessageRecord,
)


class Runtime:
    """Central runtime."""

    def __init__(self, container: Container):
        self.container = container
        self.storage = SQLiteStorage()
        self._assistants = {}
        self._storage_sessions = {}

    def create_session(
        self,
        title: str = "New Session",
    ) -> str:

        session_id = session_manager.create()

        self._assistants[session_id] = (
            self.container.assistant()
        )

        storage_session = self.storage.create_session(
            title=title,
        )

        self._storage_sessions[session_id] = (
            storage_session.id
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

        storage_session = self._storage_sessions.get(
            session_id
        )

        if storage_session is not None:

            self.storage.save_message(
                MessageRecord(
                    session_id=storage_session,
                    role="user",
                    content=message,
                )
            )

        response = assistant.chat(message)

        if storage_session is not None:

            self.storage.save_message(
                MessageRecord(
                    session_id=storage_session,
                    role="assistant",
                    content=response,
                )
            )

        return response

    def history(
        self,
        session_id: str,
    ):

        assistant = self._assistants.get(session_id)

        if assistant is None:
            raise ValueError("Invalid session.")

        return assistant.history()

    def storage_history(
        self,
        session_id: str,
    ):

        storage_session = self._storage_sessions.get(
            session_id
        )

        if storage_session is None:
            raise ValueError("Invalid session.")

        return self.storage.load_messages(
            storage_session
        )

    def list_storage_sessions(self):

        return self.storage.list_sessions()

    def delete_session(
        self,
        session_id: str,
    ):

        self._assistants.pop(
            session_id,
            None,
        )

        storage_session = self._storage_sessions.pop(
            session_id,
            None,
        )

        if storage_session:

            self.storage.delete_session(
                storage_session
            )

        return session_manager.delete(
            session_id
        )
