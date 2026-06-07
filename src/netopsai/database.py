import json
import sqlite3
from pathlib import Path
from datetime import datetime


def get_connection(db_path: Path):
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(db_path)


def init_db(db_path: Path) -> None:
    with get_connection(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS query_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                sources TEXT,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


def log_query(db_path: Path, question: str, answer: str, sources: list[dict]) -> None:
    with get_connection(db_path) as conn:
        conn.execute(
            """
            INSERT INTO query_logs (question, answer, sources, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                question,
                answer,
                json.dumps(sources),
                datetime.utcnow().isoformat(timespec="seconds") + "Z",
            ),
        )
        conn.commit()


def get_recent_queries(db_path: Path, limit: int = 10) -> list[dict]:
    init_db(db_path)

    with get_connection(db_path) as conn:
        rows = conn.execute(
            """
            SELECT question, answer, sources, created_at
            FROM query_logs
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [
        {
            "question": row[0],
            "answer": row[1],
            "sources": json.loads(row[2] or "[]"),
            "created_at": row[3],
        }
        for row in rows
    ]
