# Changelog

## [prototype-4] - 2026-04-19

### Implemented (Deliverable 5 — Scenario 4: Report Email Smart Notifications)

#### Scenario 4 Acceptance Flow
- Replaced the previous Scenario 4 stub with an implemented **Report Email Smart Notifications** acceptance scenario.
- The scenario logs in, saves a Report Email in Settings, runs a critical payment failure, verifies the Smart Notification recipient/reason/delivery on the results page, and confirms notification metadata is stored in SQLite.
- Added Selenium step definitions in `acceptance_tests/steps/ai_capabilities_steps.py`; all previous `NotImplementedError` stubs were removed.
- Updated `acceptance_tests/environment.py` to use an acceptance-only temporary SQLite database for Behave runs, preventing stale local `testflow.db` schemas from causing missing-table errors.

#### Smart Notification Test Coverage
- Added unit tests for `src/notifications.py`, including passed-run suppression, application-bug triggering, noncritical suppression, urgent timeout matching, SMTP success, and SMTP failure fallback.
- Added integration tests for Scenario 4 covering Report Email persistence, configured-recipient notification delivery, fallback to the logged-in user when no Report Email is set, and suppressed noncritical failures.
- Added database coverage for persisted notification recipient and reason fields on `test_runs`.

#### Documentation & Environment
- Updated `README.md` with clear Scenario 4 acceptance-test instructions, Scenario 4 unit/integration test commands, updated all-scenarios acceptance command, and coverage requirements.
- Documented Scenario 4 environment requirements: Docker/Chromium is enough for acceptance tests; real SMTP delivery is optional and controlled by `TESTFLOW_SMTP_*` variables.

## [prototype-3] - 2026-03-27

### Implemented (Deliverable 4 — Scenario 3: Intelligent Failure Diagnosis)

#### AI Failure Analyzer (`src/failure_analyzer.py`)
- **Gemini LLM-powered failure analysis**: Sends full failure context (error message, page state, available elements, test steps, expected outcome) to Gemini for root cause analysis.
- **Three-category classification**: Categorizes failures as `test_design` (wrong steps/selectors), `application_bug` (app not functioning correctly), or `environment` (network/timeout/infra issues).
- **Structured diagnosis output**: Returns summary, detailed explanation, actionable suggestion, and proposed fix for each failure.
- **Rule-based fallback**: When Gemini is unavailable, uses pattern matching on error messages to classify failures and provide sensible recommendations.

#### Actionable Diagnosis UI (`src/templates/test_results.html`)
- **Category badges**: Color-coded failure type indicators (yellow = test design, red = app bug, blue = environment).
- **"Apply Suggested Fix" button**: One-click applies AI-proposed test step improvements, resets test status to "Not Run".
- **"Edit Test Manually" button**: Opens test editor for manual adjustments.
- **"Re-run / Retry Test" button**: Re-executes test after application or environment fix.
- **Proposed fix display**: Shows improved test steps (for test design issues) or application fix description (for app bugs) in a styled code block.

#### Settings & Configuration (`/settings`)
- **Report email**: Users configure their email address for test failure notifications.
- **Saved applications**: Store target applications with their authentication credentials (username/password or API token). Credentials are stored separately from tests and injected automatically during execution.
- **Settings database tables**: New `settings` (key-value) and `saved_apps` (name, URL, auth_type, credentials) tables in SQLite.

#### Test Management Improvements
- **Edit test page** (`/edit-test/<id>`): View and modify test name, URL, steps, and expected outcome.
- **Clickable test names**: Test names in the list are links that navigate to the edit/details page.
- **Run All Tests** (`/run-all-tests`): Execute all saved tests sequentially with a summary of results.
- **Saved app dropdown**: Test creation form shows a dropdown of saved applications for quick URL selection.
- **Apply fix route** (`/apply-fix/<id>`): Applies AI-suggested test improvements and resets status.

### Changed
- **Test runner** (`src/test_runner.py`): Integrated `failure_analyzer.py` for structured diagnosis instead of plain-text error messages. All failure paths now return categorized diagnosis dicts.
- **Database** (`src/db.py`): Added `settings`, `saved_apps` tables. Diagnosis field now stores JSON (backward-compatible with legacy plain text). Added helpers: `get/set_setting`, `insert/get/update/delete_saved_app`, `update_test`.
- **App routes** (`src/app.py`): Added `/settings`, `/edit-test`, `/apply-fix`, `/run-all-tests` routes. Updated imports for new DB functions.
- **Navigation**: All templates now include Settings link in navbar.
- **Simulation mode**: `_simulate_execution()` now returns structured diagnosis dicts matching the Scenario 3 format.

## [prototype-2] - 2026-03-13

### Implemented (Deliverable 3 — Scenario 2: Test Execution and Monitoring)

#### Real Test Execution Engine (Selenium + BeautifulSoup + Gemini LLM)
- **Test runner** (`src/test_runner.py`): Real browser-driven test execution engine that launches headless Chrome, navigates to the target application, discovers page elements with BeautifulSoup, and executes Selenium actions. Takes real screenshots after each step, measures actual page load times, and detects real pass/fail based on execution outcomes. Generates diagnostic info from actual page state on failure.
- **LLM step parser** (`src/llm_step_parser.py`): Integrates Google Gemini API to translate free-form natural language test steps into structured Selenium commands. Sends discovered page elements + user steps to the LLM and receives back action dicts (`navigate`, `enter`, `click`, `wait`, `verify`, `select`).
- **Site crawler** (`src/site_crawler.py`): Multi-page crawler using Selenium + BeautifulSoup that discovers all interactive elements (forms, inputs, buttons, links) across 1-5 pages. Supports auto-login when user provides credentials, with priority-based link following.
- **Scenario generator** (`src/scenario_generator.py`): Sends crawled site maps to Gemini LLM to auto-generate test scenarios. Supports configurable complexity (simple/medium/complex), focus areas (authentication, CRUD, navigation, error handling, search, forms), and custom user notes.

#### Test Execution Infrastructure (Scenario 2)
- **Test runs database table** (`src/db.py`): `test_runs` table stores execution results with status, execution_time, failure_message, diagnosis, screenshots (JSON), performance metrics (JSON), and email_sent flag.
- **Database helpers** (`src/db.py`): `get_test_by_id()`, `update_test_status()`, `insert_test_run()`, `get_test_run()`, `get_latest_test_run()` — all used by Scenario 2 routes.
- **Results template** (`src/templates/test_results.html`): Displays execution status, time, real screenshot images (clickable, with fallback placeholders), performance metrics table, failure details, AI diagnosis, and email notification indicator.
- **Execution routes** (`src/app.py`): `POST /run-test/<id>` executes a test against the real target application and redirects to `GET /test-results/<id>` which displays the results.

#### Auto-Discovery Feature (Beyond Scenario 2)
- **Discover page** (`src/templates/discover.html`): Users enter a URL and optional notes (credentials, focus areas), and the system crawls the app and auto-generates test scenarios via Gemini LLM. Users can review, edit, select/deselect, then save chosen scenarios.
- **Discover routes** (`src/app.py`: `/discover`, `/save-discovered`): Orchestrate crawling, LLM generation, and saving of discovered test scenarios.

#### Acceptance Tests for Scenario 2
- **Step definitions** (`acceptance_tests/steps/test_execution_steps.py`): 17 Selenium-based steps for Scenario 2A (passing test with status, time, screenshots, metrics) and Scenario 2B (failing test with error message, failure screenshot, AI diagnosis, email notification).
- **Environment setup** (`acceptance_tests/environment.py`): Sets `TESTFLOW_SIMULATE=1` for deterministic results, auto-detects Chrome location (Docker vs local), increased timeouts for reliability.

### Changed

- **Test list page** (`src/templates/test_list.html`): Added "Run Test" button with loading overlay (spinner, progress steps, elapsed timer), "AI Discover" button, and "Results" link per test row.
- **Password hashing** (`src/db.py`): Changed from `scrypt` to `pbkdf2:sha256` method for Python 3.13 compatibility.
- **App module docstring** (`src/app.py`): Updated to describe both Scenario 1 and Scenario 2 flows including real execution and simulation fallback.
- **Requirements** (`requirements.txt`): Added `google-genai` for Gemini LLM integration.

### Notes

- Real execution requires: Chrome/Chromium installed, Gemini API key in `.claude/.config`, and a reachable target application (e.g., Kanboard on localhost:8080).
- Acceptance tests use a deterministic fallback (`TESTFLOW_SIMULATE=1`) in Docker/CI where the Gemini API and target apps are unavailable.
- Email notification is displayed on the results page (not actually sent via SMTP).
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
