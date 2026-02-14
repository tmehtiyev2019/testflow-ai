# Changelog

## [prototype-1] - 2026-02-14

### Implemented (Deliverable 2 — Scenario 1: Test Creation)

- **Flask web application** (`testflow/app.py`) with routes for login, test creation form, and test list page.
- **SQLite database** (`testflow/db.py`) storing test scenarios with name, URL, steps, expected outcome, and status (default "Not Run").
- **HTML templates** (`testflow/templates/`) for login, create test, and test list pages.
- **Selenium step definitions** (`acceptance_tests/steps/test_creation_steps.py`) driving a real headless Chromium browser against the Flask app.
- **Behave environment** (`acceptance_tests/environment.py`) starts Flask in a background thread, initializes Selenium, and resets the database between scenarios.

### Changed
- Replaced in-memory platform prototype with real Flask + SQLite + Selenium implementation.
- Added `flask>=3.0.0` to `requirements.txt`.
- Updated README with technology stack, architecture explanation, and correct expected output.

### Notes
- Only Scenario 1 is implemented in this deliverable. Scenarios 2-4 remain stubs.
