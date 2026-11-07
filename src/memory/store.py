import sqlite3
from pathlib import Path
from datetime import datetime, timezone


class MemoryStore:
    """Memória local mínima baseada em SQLite."""

    def __init__(self, db_path: str = "data/conori_memory.sqlite3") -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS conversation (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )

    def save(self, role: str, content: str) -> None:
        timestamp = datetime.now(timezone.utc).isoformat()
        with self._connect() as connection:
            connection.execute(
                "INSERT INTO conversation (role, content, created_at) VALUES (?, ?, ?)",
                (role, content, timestamp),
            )

    def recent(self, limit: int = 10):
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT role, content, created_at FROM conversation "
                "ORDER BY id DESC LIMIT ?",
                (max(1, limit),),
            ).fetchall()
        return list(reversed(rows))

    def clear(self) -> None:
        with self._connect() as connection:
            connection.execute("DELETE FROM conversation")
