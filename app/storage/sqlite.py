"""SQLite storage implementation."""

import sqlite3
from datetime import datetime

from app.storage.base import BaseStorage
from app.storage.models import (
    MessageRecord,
    SessionRecord,
)


class SQLiteStorage(BaseStorage):
    """SQLite storage backend."""

    def __init__(
        self,
        database: str = "agent.db",
    ) -> None:
        self.connection = sqlite3.connect(database)
        self.connection.row_factory = sqlite3.Row

        self._create_tables()

    def _create_tables(self) -> None:

        cursor = self.connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions(
                id TEXT PRIMARY KEY,
                title TEXT,
                created_at TEXT,
                updated_at TEXT
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS messages(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                role TEXT,
                content TEXT,
                created_at TEXT
            )
            """
        )

        self.connection.commit()

    def create_session(
        self,
        title: str = "New Session",
    ) -> SessionRecord:

        session = SessionRecord(title=title)

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO sessions
            VALUES (?, ?, ?, ?)
            """,
            (
                session.id,
                session.title,
                session.created_at.isoformat(),
                session.updated_at.isoformat(),
            ),
        )

        self.connection.commit()

        return session

    def save_message(
        self,
        message: MessageRecord,
    ) -> None:

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO messages(
                session_id,
                role,
                content,
                created_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                message.session_id,
                message.role,
                message.content,
                message.created_at.isoformat(),
            ),
        )

        self.connection.commit()

    def load_messages(
        self,
        session_id: str,
    ) -> list[MessageRecord]:

        cursor = self.connection.cursor()

        rows = cursor.execute(
            """
            SELECT *
            FROM messages
            WHERE session_id = ?
            ORDER BY id
            """,
            (session_id,),
        ).fetchall()

        return [
            MessageRecord(
                session_id=row["session_id"],
                role=row["role"],
                content=row["content"],
                created_at=datetime.fromisoformat(
                    row["created_at"]
                ),
            )
            for row in rows
        ]

    def list_sessions(
        self,
    ) -> list[SessionRecord]:

        cursor = self.connection.cursor()

        rows = cursor.execute(
            """
            SELECT *
            FROM sessions
            ORDER BY created_at DESC
            """
        ).fetchall()

        return [
            SessionRecord(
                id=row["id"],
                title=row["title"],
                created_at=datetime.fromisoformat(
                    row["created_at"]
                ),
                updated_at=datetime.fromisoformat(
                    row["updated_at"]
                ),
            )
            for row in rows
        ]

    def delete_session(
        self,
        session_id: str,
    ) -> bool:

        cursor = self.connection.cursor()

        cursor.execute(
            "DELETE FROM messages WHERE session_id = ?",
            (session_id,),
        )

        cursor.execute(
            "DELETE FROM sessions WHERE id = ?",
            (session_id,),
        )

        self.connection.commit()

        return cursor.rowcount > 0

    def close(self) -> None:
        """Close the database connection."""
        self.connection.close()
