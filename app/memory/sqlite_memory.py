import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Iterator, List

from app.schemas.chat import Message


class SQLiteChatMemory:
    table_name = "chat_messages"

    def __init__(self, database_url: str) -> None:
        if not database_url.startswith("sqlite"):
            raise ValueError("SQLiteChatMemory only supports SQLite URLs")
        self._db_path = self._extract_sqlite_path(database_url)
        Path(self._db_path).parent.mkdir(parents=True, exist_ok=True)
        self._ensure_schema()

    @staticmethod
    def _extract_sqlite_path(database_url: str) -> str:
        if database_url.startswith("sqlite:///"):
            return database_url.replace("sqlite:///", "", 1)
        if database_url == "sqlite://":
            return ":memory:"
        raise ValueError(f"Unsupported SQLite URL format: {database_url}")

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self._db_path, check_same_thread=False)
        try:
            yield conn
        finally:
            conn.close()

    def _ensure_schema(self) -> None:
        with self._connect() as conn:
            conn.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def get_history(self, session_id: str) -> list[Message]:
        with self._connect() as conn:
            cursor = conn.execute(
                f"SELECT role, content, timestamp FROM {self.table_name} WHERE session_id = ? ORDER BY id ASC",
                (session_id,),
            )
            rows = cursor.fetchall()

        return [
            Message(role=row[0], content=row[1], timestamp=datetime.fromisoformat(row[2]))
            for row in rows
        ]

    def append_messages(self, session_id: str, messages: list[Message]) -> list[Message]:
        with self._connect() as conn:
            conn.executemany(
                f"INSERT INTO {self.table_name} (session_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
                [
                    (
                        session_id,
                        message.role,
                        message.content,
                        message.timestamp.isoformat(),
                    )
                    for message in messages
                ],
            )
            conn.commit()

        return self.get_history(session_id)

    def set_history(self, session_id: str, messages: list[Message]) -> list[Message]:
        with self._connect() as conn:
            conn.execute(f"DELETE FROM {self.table_name} WHERE session_id = ?", (session_id,))
            conn.executemany(
                f"INSERT INTO {self.table_name} (session_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
                [
                    (
                        session_id,
                        message.role,
                        message.content,
                        message.timestamp.isoformat(),
                    )
                    for message in messages
                ],
            )
            conn.commit()

        return self.get_history(session_id)

    def clear(self, session_id: str) -> None:
        with self._connect() as conn:
            conn.execute(f"DELETE FROM {self.table_name} WHERE session_id = ?", (session_id,))
            conn.commit()
