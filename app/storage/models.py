"""Storage models."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4


def generate_id() -> str:
    """Generate a unique identifier."""
    return str(uuid4())


def utc_now() -> datetime:
    """Return the current UTC time."""
    return datetime.now(UTC)


@dataclass(slots=True)
class SessionRecord:
    """Represents a conversation session."""

    id: str = field(default_factory=generate_id)
    title: str = "New Session"
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)


@dataclass(slots=True)
class MessageRecord:
    """Represents one stored message."""

    session_id: str
    role: str
    content: str
    created_at: datetime = field(default_factory=utc_now)


@dataclass(slots=True)
class StorageResult:
    """Standard storage operation result."""

    success: bool
    message: str = ""
    data: Any = None
