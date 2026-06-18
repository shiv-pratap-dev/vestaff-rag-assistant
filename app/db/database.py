"""
Database utilities.

Responsible for:
1. Creating SQLite connections
2. Initializing database tables
3. Managing database setup for the application
"""

import sqlite3

from app.core.config import settings


def get_connection() -> sqlite3.Connection:
    """
    Creates and returns a SQLite database connection.
    """

    return sqlite3.connect(settings.DB_PATH)


def init_db():
    """
    Creates all required database tables
    if they do not already exist.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS query_logs (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            session_id TEXT,

            question TEXT NOT NULL,

            answer TEXT NOT NULL,

            confidence_score REAL,

            latency_ms REAL,

            answer_found INTEGER,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """
    )

    conn.commit()
    conn.close()