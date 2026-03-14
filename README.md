# Black-Box End-to-End Testing SaaS Platform

## Project Description

A SaaS platform that tests applications from the user's perspective without requiring access to internal code. The platform validates complete user workflows across web applications, APIs, and mobile applications using AI-powered intelligent testing capabilities.

### Key Features

- **Natural Language Test Creation**: Define test scenarios in plain English without coding
- **Automated Workflow Execution**: Execute multi-step user journeys with screenshot capture
- **AI-Powered Test Intelligence**: Self-healing tests that adapt to UI changes and provide intelligent failure diagnosis
- **Comprehensive Reporting**: Visual diff reports, performance metrics, and execution logs
- **Smart Notifications**: Real-time alerts for test failures with actionable insights

## Setup

### 1. Install Docker
- **macOS/Windows**: Download [Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Linux**: Follow [Docker installation guide](https://docs.docker.com/engine/install/)

### 2. Clone and Navigate to Project
```bash
git clone https://github.com/tmehtiyev2019/testflow-ai.git
cd testflow-ai
```

### 3. Build Docker Image
```bash
docker-compose build
```

### 4. Verify Installation
```bash
docker-compose run --rm testflow behave --version
# Expected output: behave 1.2.6
```

## Running Tests

### Run Scenario 1 (Test Creation)
```bash
docker-compose run --rm testflow behave acceptance_tests/test_creation.feature
```

Expected output:
```
1 feature passed, 0 failed, 0 skipped
1 scenario passed, 0 failed, 0 skipped
9 steps passed, 0 failed, 0 skipped
```

### Run Scenario 2 (Test Execution and Monitoring)
```bash
docker-compose run --rm testflow behave acceptance_tests/test_execution.feature
```

Expected output:
```
1 feature passed, 0 failed, 0 skipped
2 scenarios passed, 0 failed, 0 skipped
17 steps passed, 0 failed, 0 skipped
```

### Run All Implemented Acceptance Tests (Scenarios 1 & 2)
```bash
docker-compose run --rm testflow behave acceptance_tests/test_creation.feature acceptance_tests/test_execution.feature
```

### Run All Acceptance Tests
```bash
docker-compose run --rm testflow behave acceptance_tests/
```

Note: Scenarios 3-4 are not yet implemented and will error with `NotImplementedError`.

## Technology Stack

- **Web Application**: Flask (Python) with server-side HTML templates
- **Database**: SQLite
- **Browser Automation**: Selenium + headless Chromium
- **Testing Framework**: Behave (BDD / Gherkin)
- **Containerization**: Docker

## How It Works

When tests run, the following happens inside the Docker container:

1. Behave starts and `environment.py` launches a Flask server on port 5000 in a background thread
2. A headless Chromium browser is opened via Selenium
3. Step definitions use Selenium to navigate to pages, fill forms, and click buttons on the real Flask app
4. Flask saves data to SQLite and renders HTML pages
5. **Scenario 1**: Selenium creates a test via the form and verifies it appears in the list
6. **Scenario 2**: Step definitions pre-seed test data, click "Run Test", and verify execution results (status, time, screenshots, metrics, failure details, AI diagnosis)
7. After tests complete, the browser and server shut down

## Acceptance Test Scenarios

### Scenario 1: Test Creation (Implemented)
- **User Story**: As a QA engineer, I want to create test scenarios in natural language
- **Flow**: Login → Navigate to "Create Test" → Fill form → Save → See confirmation → Test appears in list

### Scenario 2: Test Execution and Monitoring (Implemented)
- **User Story**: As a product manager, I want to execute tests and monitor results
- **Scenario 2A**: Run a passing test → see status "Passed", execution time, per-step screenshots, performance metrics
- **Scenario 2B**: Run a failing test → see status "Failed", error message, failure screenshot, AI diagnosis, email notification

### Scenario 3: Failure Diagnosis (Not yet implemented)
- **User Story**: As a product manager, I want detailed failure reports

### Scenario 4: SWAP CHALLENGE - Self-Healing Tests (Not yet implemented)
- **User Story**: As a development team, I want tests to adapt to UI changes automatically

## Project Structure

```
testflow-ai/
├── src/                                 # Source code
│   ├── __init__.py
│   ├── app.py                           # Flask application (routes, views)
│   ├── db.py                            # SQLite database helpers
│   └── templates/
│       ├── login.html                   # Login page
│       ├── create_test.html             # Test creation form
│       ├── test_list.html               # Test list with status and Run buttons
│       └── test_results.html            # Test execution results (Scenario 2)
├── acceptance_tests/                    # BDD test suite
│   ├── test_creation.feature            # Scenario 1 (Gherkin)
│   ├── test_execution.feature           # Scenarios 2 & 3 (Gherkin)
│   ├── ai_capabilities.feature          # Scenario 4 - SWAP CHALLENGE (Gherkin)
│   ├── steps/                           # Step definitions
│   │   ├── test_creation_steps.py       # Selenium-based steps for Scenario 1
│   │   ├── test_execution_steps.py      # Selenium steps for Scenario 2
│   │   └── ai_capabilities_steps.py     # Stubs for Scenario 4
│   └── environment.py                   # Flask + Selenium setup/teardown
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── CHANGELOG.md
└── PRODUCT_SPECIFICATION.md
```

## Troubleshooting

### "docker: command not found"
Make sure Docker is installed and running. On macOS/Windows, check that Docker Desktop is open.

### Container build fails
```bash
docker-compose build --no-cache
```

### Tests not reflecting code changes
```bash
docker-compose down
docker-compose build
docker-compose run --rm testflow behave acceptance_tests/test_creation.feature
```
