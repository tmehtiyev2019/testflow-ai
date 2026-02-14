# Changelog

## [prototype-1] - 2026-02-14

### Implemented (Deliverable 2 — Scenario 1: Test Creation)

- **Flask web application** (`src/app.py`) with routes for login, test creation form, and test list page.
- **SQLite database** (`src/db.py`) storing test scenarios with name, URL, steps, expected outcome, and status (default "Not Run").
- **HTML templates** (`src/templates/`) for login, create test, and test list pages.
- **Selenium step definitions** (`test/steps/test_creation_steps.py`) driving a real headless Chromium browser against the Flask app.
- **Behave environment** (`test/environment.py`) starts Flask in a background thread, initializes Selenium, and resets the database between scenarios.

### Changed
- Replaced in-memory platform prototype with real Flask + SQLite + Selenium implementation.
- Added `flask>=3.0.0` to `requirements.txt`.
- Renamed directories to match rubric: `src/`, `test/`, `test/steps/`.
- Updated README with technology stack, architecture explanation, and correct expected output.

### Notes
- Only Scenario 1 is implemented in this deliverable. Scenarios 2-4 remain stubs.
