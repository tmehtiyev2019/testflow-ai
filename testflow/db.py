"""SQLite database helpers for Scenario 1 (Test Creation).

This module provides all database operations needed by Scenario 1.
The acceptance test flow is:
    login -> navigate to "Create Test" -> fill form -> save -> see test in list

Schema — test_scenarios table:
    id               INTEGER  Primary key (auto-increment).
    name             TEXT     Test name entered by user.          (Scenario 1: step "I enter the test name")
    application_url  TEXT     Target app URL.                     (Scenario 1: step "I enter the application URL")
    steps_raw        TEXT     Natural language test steps.        (Scenario 1: step "I provide the test steps")
    expected_outcome TEXT     Expected result of the test.        (Scenario 1: step "I set expected outcome")
    status           TEXT     Defaults to "Not Run".              (Scenario 1: step "test should appear ... with status")
"""

import sqlite3
import os

# Default DB path; can be overridden via environment variable for testing.
DB_PATH = os.environ.get("TESTFLOW_DB", "testflow.db")


def get_connection() -> sqlite3.Connection:
    """Return a connection to the SQLite database.

    Uses sqlite3.Row so rows can be accessed by column name.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create the test_scenarios table if it does not exist.

    Called once at Flask app startup (Scenario 1).
    """
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
    """Drop and recreate the table.

    Called in environment.py before_scenario to ensure each test starts
    with a clean database.
    """
    conn = get_connection()
    conn.execute("DROP TABLE IF EXISTS test_scenarios")
    conn.commit()
    conn.close()
    init_db()


def insert_test(name: str, application_url: str, steps_raw: str, expected_outcome: str) -> int:
    """Insert a new test scenario into the database. Returns the new row id.

    Scenario 1: called when the user clicks "Save Test" on the create test form.
    The status column defaults to "Not Run".
    """
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
    """Return all saved test scenarios as a list of dicts.

    Scenario 1: used by the /tests route to render the test list page.
    Each dict contains: id, name, application_url, steps_raw, expected_outcome, status.
    """
    conn = get_connection()
    rows = conn.execute("SELECT * FROM test_scenarios ORDER BY id").fetchall()
    conn.close()
    return [dict(row) for row in rows]
