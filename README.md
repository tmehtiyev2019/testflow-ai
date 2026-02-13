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

### Deliverable 2 (Prototype-1)
- Scenario 1 (**Test Creation**) is implemented and should pass.
- Other scenarios are still stubbed and may error if run.


### Run All Acceptance Tests
```bash
docker-compose run --rm testflow behave acceptance_tests/
```

### Run Individual Features
```bash
# Test Creation
docker-compose run --rm testflow behave acceptance_tests/test_creation.feature

# Test Execution
docker-compose run --rm testflow behave acceptance_tests/test_execution.feature

# AI Capabilities (SWAP CHALLENGE)
docker-compose run --rm testflow behave acceptance_tests/ai_capabilities.feature
```

### Expected Output

For Deliverable 2, run Scenario 1 only:

```bash
docker-compose run --rm testflow behave acceptance_tests/test_creation.feature
```

Expected: Scenario 1 passes.

Running all acceptance tests may still error because scenarios 2–4 are not implemented in this deliverable.


## Acceptance Test Scenarios

### Scenario 1: Test Creation
- **Feature**: Test Scenario Creation
- **User Story**: As a QA engineer, I want to create test scenarios in natural language
- **Scope**: Create a test with name, URL, steps, and expected outcomes

### Scenario 2: Test Execution and Results
- **Feature**: Test Execution and Monitoring
- **User Story**: As a product manager, I want to execute tests and monitor results
- **Scope**: Run test, view pass/fail status, screenshots, and performance metrics

### Scenario 3: Failure Diagnosis
- **Feature**: Test Execution and Monitoring
- **User Story**: As a product manager, I want detailed failure reports
- **Scope**: Execute failing test, view failure message, AI diagnosis, and notifications

### Scenario 4: SWAP CHALLENGE - Self-Healing Tests
- **Feature**: AI-Powered Testing Capabilities
- **User Story**: As a development team, I want tests to adapt to UI changes automatically
- **Scope**: Test detects UI change, AI identifies new selector, test auto-heals

## Project Structure

```
testflow-ai/
├── acceptance_tests/
│   ├── test_creation.feature          # Test scenario creation feature
│   ├── test_execution.feature         # Test execution and monitoring feature
│   ├── ai_capabilities.feature        # AI-powered testing (SWAP CHALLENGE)
│   ├── steps/
│   │   ├── test_creation_steps.py     # Step definitions for test creation
│   │   ├── test_execution_steps.py    # Step definitions for execution
│   │   └── ai_capabilities_steps.py   # Step definitions for AI features
│   └── environment.py                 # Behave test environment configuration
├── Dockerfile                         # Docker image definition
├── docker-compose.yml                 # Docker Compose configuration
├── README.md                          # This file
├── PRODUCT_SPECIFICATION.md           # Detailed product specification
└── requirements.txt                   # Python dependencies
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
docker-compose run --rm testflow behave acceptance_tests/
```
