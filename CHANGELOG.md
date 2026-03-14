# Changelog

## [prototype-2] - 2026-03-13

### Implemented (Deliverable 3 — Scenario 2: Test Execution and Monitoring)

- **Test execution simulation** (`src/app.py`): `POST /run-test/<id>` route simulates running a saved test scenario, generates mock screenshots, performance metrics, and determines pass/fail outcome.
- **Test results page** (`src/app.py`): `GET /test-results/<id>` route displays execution results including status, execution time, per-step screenshots, and page load metrics.
- **Failure reporting** (`src/app.py`): failed tests display error message, failure-point screenshot, AI-powered diagnosis, and email notification status.
- **Test runs database table** (`src/db.py`): new `test_runs` table stores execution results with status, execution_time, failure_message, diagnosis, screenshots (JSON), performance metrics (JSON), and email_sent flag.
- **Database helpers** (`src/db.py`): added `get_test_by_id()`, `update_test_status()`, `insert_test_run()`, `get_test_run()`, `get_latest_test_run()`.
- **Results template** (`src/templates/test_results.html`): new page showing execution status, time, step screenshots, performance metrics table, failure details, AI diagnosis, and email notification indicator.
- **Selenium step definitions** (`acceptance_tests/steps/test_execution_steps.py`): 17 steps implemented for both sub-scenarios (2A: passing test, 2B: failing test with diagnosis).

### Changed

- **Test list page** (`src/templates/test_list.html`): added "Actions" column with "Run Test" button and "Results" link per test row.
- **Database reset** (`src/db.py`): `reset_db()` now drops both `test_runs` and `test_scenarios` tables for clean test state.
- **App imports** (`src/app.py`): added imports for new database functions and standard library modules (`time`, `random`, `json`).

### Notes

- Test execution is simulated (no real browser automation against external sites). Pass/fail is determined by the test's expected_outcome content.
- Screenshots are placeholder paths; performance metrics are randomly generated.
- Email notification is simulated (displayed on results page, not actually sent).
- Scenarios 3-4 remain stubs.

## [prototype-1] - 2026-02-14

### Implemented (Deliverable 2 — Scenario 1: Test Creation)

- **Flask web application** (`src/app.py`) with routes for login, test creation form, and test list page.
- **SQLite database** (`src/db.py`) storing test scenarios with name, URL, steps, expected outcome, and status (default "Not Run").
- **HTML templates** (`src/templates/`) for login, create test, and test list pages.
- **Selenium step definitions** (`acceptance_tests/steps/test_creation_steps.py`) driving a real headless Chromium browser against the Flask app.
- **Behave environment** (`acceptance_tests/environment.py`) starts Flask in a background thread, initializes Selenium, and resets the database between scenarios.

### Changed
- Replaced in-memory platform prototype with real Flask + SQLite + Selenium implementation.
- Added `flask>=3.0.0` to `requirements.txt`.
- Renamed source code directory to `src/`.
- Updated README with technology stack, architecture explanation, and correct expected output.

### Notes
- Only Scenario 1 is implemented in this deliverable. Scenarios 2-4 remain stubs.
