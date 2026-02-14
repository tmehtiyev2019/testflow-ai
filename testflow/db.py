"""SQLite database helpers for Scenario 1 (Test Creation).

Schema:
    test_scenarios — stores tests created via the "Create Test" page.
    Each row maps to one saved test scenario with a default status of "Not Run".
"""

import sqlite3
import os

# Default DB path; can be overridden for testing.
DB_PATH = os.environ.get("TESTFLOW_DB", "testflow.db")


def get_connection() -> sqlite3.Connection:
    """Return a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create the test_scenarios table if it does not exist."""
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS test_scenarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            application_url TEXT NOT NULL,
            steps_raw TEXT NOT NULL,
            expected_outcome TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Not Run'
        )
        """
    )
    conn.commit()
    conn.close()


def reset_db() -> None:
    """Drop and recreate the table. Used between test scenarios for clean state."""
    conn = get_connection()
    conn.execute("DROP TABLE IF EXISTS test_scenarios")
    conn.commit()
    conn.close()
    init_db()


def insert_test(name: str, application_url: str, steps_raw: str, expected_outcome: str) -> int:
    """Insert a new test scenario. Returns the new row id."""
    conn = get_connection()
    cursor = conn.execute(
        """
        INSERT INTO test_scenarios (name, application_url, steps_raw, expected_outcome)
        VALUES (?, ?, ?, ?)
        """,
        (name, application_url, steps_raw.strip(), expected_outcome.strip()),
    )
    conn.commit()
    row_id = cursor.lastrowid
    conn.close()
    return row_id


def get_all_tests() -> list[dict]:
    """Return all test scenarios as a list of dicts."""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM test_scenarios ORDER BY id").fetchall()
    conn.close()
    return [dict(row) for row in rows]
