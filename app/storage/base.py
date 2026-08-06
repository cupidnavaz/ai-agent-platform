"""Base storage interface."""

from abc import ABC, abstractmethod

from app.storage.models import (
    MessageRecord,
    SessionRecord,
)


class BaseStorage(ABC):
    """Abstract storage interface."""

    @abstractmethod
    def create_session(
        self,
        title: str = "New Session",
    ) -> SessionRecord:
        """Create a new session."""
        raise NotImplementedError

    @abstractmethod
    def save_message(
        self,
        message: MessageRecord,
    ) -> None:
        """Save a message."""
        raise NotImplementedError

    @abstractmethod
    def load_messages(
        self,
        session_id: str,
    ) -> list[MessageRecord]:
        """Load session messages."""
        raise NotImplementedError

    @abstractmethod
    def list_sessions(
        self,
    ) -> list[SessionRecord]:
        """List sessions."""
        raise NotImplementedError

    @abstractmethod
    def delete_session(
        self,
        session_id: str,
    ) -> bool:
        """Delete a session."""
        raise NotImplementedError
