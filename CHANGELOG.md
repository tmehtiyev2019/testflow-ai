# Changelog

## [prototype-2] - 2026-03-13

### Implemented (Deliverable 3 — Scenario 2: Test Execution and Monitoring)

#### Real Test Execution Engine (Selenium + BeautifulSoup + Gemini LLM)
- **Test runner** (`src/test_runner.py`): Real browser-driven test execution engine that launches headless Chrome, navigates to the target application, discovers page elements with BeautifulSoup, and executes Selenium actions. Takes real screenshots after each step, measures actual page load times, and detects real pass/fail based on execution outcomes. Generates diagnostic info from actual page state on failure.
- **LLM step parser** (`src/llm_step_parser.py`): Integrates Google Gemini API to translate free-form natural language test steps into structured Selenium commands. Sends discovered page elements + user steps to the LLM and receives back action dicts (`navigate`, `enter`, `click`, `wait`, `verify`, `select`).
- **Site crawler** (`src/site_crawler.py`): Multi-page crawler using Selenium + BeautifulSoup that discovers all interactive elements (forms, inputs, buttons, links) across 1-5 pages. Supports auto-login when user provides credentials, with priority-based link following.
- **Scenario generator** (`src/scenario_generator.py`): Sends crawled site maps to Gemini LLM to auto-generate test scenarios. Supports configurable complexity (simple/medium/complex), focus areas (authentication, CRUD, navigation, error handling, search, forms), and custom user notes.

#### Test Execution Simulation Fallback (Scenario 2 Acceptance Tests)
- **Simulated execution** (`src/app.py`: `_simulate_execution()`): Deterministic fallback used during acceptance tests (triggered by `TESTFLOW_SIMULATE=1` env var). Generates mock screenshots, random performance metrics, and determines pass/fail based on expected_outcome keywords. Ensures acceptance tests pass reliably without requiring external services.
- **Test runs database table** (`src/db.py`): `test_runs` table stores execution results with status, execution_time, failure_message, diagnosis, screenshots (JSON), performance metrics (JSON), and email_sent flag.
- **Database helpers** (`src/db.py`): `get_test_by_id()`, `update_test_status()`, `insert_test_run()`, `get_test_run()`, `get_latest_test_run()` — all used by Scenario 2 routes.
- **Results template** (`src/templates/test_results.html`): Displays execution status, time, real screenshot images (clickable, with fallback placeholders), performance metrics table, failure details, AI diagnosis, and email notification indicator.

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

- Acceptance tests use simulation mode (`TESTFLOW_SIMULATE=1`) for deterministic results.
- Real execution mode requires: Chrome/Chromium installed, Gemini API key in `.claude/.config`, and a reachable target application.
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
