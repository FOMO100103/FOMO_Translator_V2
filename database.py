from __future__ import annotations
import sqlite3
from pathlib import Path
from datetime import datetime, timezone
from .config import ROOT_DIR

DB_PATH = ROOT_DIR / "fomo_history.db"

def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS translations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                mode TEXT NOT NULL,
                source_text TEXT NOT NULL,
                translated_text TEXT NOT NULL,
                model TEXT NOT NULL
            )
        """)

def save_translation(mode: str, source_text: str, translated_text: str, model: str):
    with _connect() as conn:
        conn.execute(
            "INSERT INTO translations (created_at, mode, source_text, translated_text, model) VALUES (?, ?, ?, ?, ?)",
            (datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
             mode, source_text, translated_text, model)
        )

def get_history(limit: int = 100):
    with _connect() as conn:
        rows = conn.execute(
            "SELECT * FROM translations ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(row) for row in rows]

def clear_history():
    with _connect() as conn:
        conn.execute("DELETE FROM translations")
