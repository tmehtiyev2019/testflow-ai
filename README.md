# Black-Box End-to-End Testing SaaS Platform

## Project Description

A SaaS platform that tests applications from the user's perspective without requiring access to internal code. The platform validates complete user workflows across web applications, APIs, and mobile applications using AI-powered intelligent testing capabilities.

### Key Features

- **Natural Language Test Creation**: Define test scenarios in plain English without coding
- **Automated Workflow Execution**: Execute multi-step user journeys with screenshot capture
- **AI-Powered Test Intelligence**: Self-healing tests that adapt to UI changes and provide intelligent failure diagnosis
- **Comprehensive Reporting**: Visual diff reports, performance metrics, and execution logs
- **Multi-Channel Testing**: Support for web apps, APIs, and mobile applications
- **Smart Notifications**: Real-time alerts for test failures with actionable insights

### Target Users

- **Primary**: QA engineers, product managers, and small development teams needing workflow validation without extensive testing infrastructure
- **Secondary**: Non-technical stakeholders monitoring critical user journeys (checkout, signup, login flows)

### Core Capabilities

1. **Test Creation**: Create tests using natural language or JSON format
2. **Test Execution**: On-demand, scheduled, or deployment-triggered test runs
3. **Visual Testing**: Screenshot/video capture at each step with visual diff analysis
4. **Performance Monitoring**: Response time tracking and performance metrics
5. **AI Diagnosis**: Intelligent root cause analysis beyond simple pass/fail
6. **Self-Healing**: Tests automatically adapt to minor UI changes

## Environment Requirements

### System Requirements
- **Docker**: 20.10 or higher
- **Docker Compose**: 2.0 or higher (usually included with Docker Desktop)
- **Operating System**: macOS, Linux, or Windows with WSL2

### What's Included in Docker Container
- Python 3.11
- Behave testing framework
- Selenium WebDriver
- Google Chrome (for browser automation)
- All project dependencies

### Installation

1. **Install Docker**:
   - **macOS/Windows**: Download [Docker Desktop](https://www.docker.com/products/docker-desktop)
   - **Linux**: Follow [Docker installation guide](https://docs.docker.com/engine/install/)

2. **Verify Docker installation**:
   ```bash
   docker --version
   docker-compose --version
   ```

3. **Clone the repository**:
   ```bash
   git clone https://github.com/tmehtiyev2019/testflow-ai.git
   cd testflow-ai
   ```

4. **Build the Docker image**:
   ```bash
   docker-compose build
   ```

5. **Verify installation**:
   ```bash
   docker-compose run --rm testflow behave --version
   ```
   Expected output: `behave 1.2.6`

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
├── Makefile                           # Shortcut commands for Docker
├── .dockerignore                      # Files to exclude from Docker build
├── .gitignore                         # Git ignore patterns
├── README.md                          # This file
├── PRODUCT_SPECIFICATION.md           # Detailed product vision and features
├── QUICK_START.md                     # Quick reference guide
└── requirements.txt                   # Python dependencies
```

## Instructions to Run Acceptance Tests

### Prerequisites Check

Before running tests, ensure Docker is properly configured:

```bash
# Verify Docker is installed and running
docker --version
docker-compose --version

# Build the Docker image (first time only)
docker-compose build
```

### Running All Acceptance Tests

To run all acceptance tests in the project:

```bash
docker-compose run --rm testflow behave acceptance_tests/
```

**Expected Output**: All tests should initially **FAIL** with `NotImplementedError` exceptions, as the step implementations are stubs.

### Running Specific Feature Files

To run tests for a specific feature:

```bash
# Test Creation feature
docker-compose run --rm testflow behave acceptance_tests/test_creation.feature

# Test Execution feature
docker-compose run --rm testflow behave acceptance_tests/test_execution.feature

# AI Capabilities feature (includes SWAP CHALLENGE)
docker-compose run --rm testflow behave acceptance_tests/ai_capabilities.feature
```

### Running Specific Scenarios

To run a specific scenario by name:

```bash
# Run a specific scenario
docker-compose run --rm testflow behave acceptance_tests/ --name "Create a simple web application test using natural language"

# Run the SWAP CHALLENGE scenario
docker-compose run --rm testflow behave acceptance_tests/ --name "SWAP CHALLENGE"
```

### Running with Verbose Output

For detailed step-by-step output:

```bash
docker-compose run --rm testflow behave acceptance_tests/ --verbose
```

### Running with Tags (Future Enhancement)

Once tags are added to scenarios, you can filter tests:

```bash
# Run only tests tagged with @critical
docker-compose run --rm testflow behave acceptance_tests/ --tags=@critical

# Skip tests tagged with @wip (work in progress)
docker-compose run --rm testflow behave acceptance_tests/ --tags=~@wip
```

### Interactive Development

To run commands inside the container interactively:

```bash
# Start a bash shell in the container
docker-compose run --rm testflow bash

# Inside the container, you can run commands directly:
behave acceptance_tests/
behave acceptance_tests/test_creation.feature
exit
```

### Test Execution Summary

After running the tests, you should see output similar to:

```
Feature: Test Scenario Creation
  Scenario: Create a simple web application test using natural language
    Given I am logged into the testing platform ... failed (NotImplementedError)

...

Failing scenarios:
  acceptance_tests/test_creation.feature:5  Create a simple web application test using natural language
  acceptance_tests/test_execution.feature:6  Execute a web application test and view results
  acceptance_tests/test_execution.feature:22  View detailed failure report when test fails
  acceptance_tests/ai_capabilities.feature:7  SWAP CHALLENGE - Self-healing test adapts to UI changes

0 features passed, 3 failed, 0 skipped
0 scenarios passed, 4 failed, 0 skipped
0 steps passed, 4 failed, 0 skipped, X undefined
```

### Generating Test Reports (Optional)

For HTML reports with Allure:

```bash
# Run tests with Allure formatter
docker-compose run --rm testflow behave acceptance_tests/ -f allure_behave.formatter:AllureFormatter -o ./reports

# Reports will be saved to ./reports directory on your host machine
# To view reports, you'll need Allure installed locally or use a report viewer
```

### Using Makefile (Optional Shortcut)

For convenience, you can use the Makefile for shorter commands:

```bash
# Show all available commands
make help

# Build Docker image
make build

# Run all tests
make test

# Run specific features
make test-creation
make test-execution
make test-swap

# Run with verbose output
make test-verbose

# Open interactive shell
make shell

# Clean up
make clean
```

### Docker Tips

```bash
# Rebuild the image after changing requirements.txt
docker-compose build --no-cache
# Or: make rebuild

# View container logs
docker-compose logs testflow

# Stop all containers
docker-compose down

# Remove all containers and volumes
docker-compose down -v

# Run a single command without keeping container
docker-compose run --rm testflow <command>
```

## Acceptance Test Scenarios

### Scenario 1: Test Creation
- **Feature**: Test Scenario Creation
- **User Story**: As a QA engineer, I want to create test scenarios in natural language
- **Scope**: Create a test with name, URL, steps, and expected outcomes
- **Verification**: Test appears in list with "Not Run" status

### Scenario 2: Test Execution and Results
- **Feature**: Test Execution and Monitoring
- **User Story**: As a product manager, I want to execute tests and monitor results
- **Scope**: Run test, view pass/fail status, screenshots, and performance metrics
- **Verification**: Test status, execution time, and screenshots are displayed

### Scenario 3: Failure Diagnosis
- **Feature**: Test Execution and Monitoring
- **User Story**: As a product manager, I want detailed failure reports
- **Scope**: Execute failing test, view failure message, AI diagnosis, and notifications
- **Verification**: Failure details, AI suggestions, and email notifications work

### Scenario 4: SWAP CHALLENGE - Self-Healing Tests
- **Feature**: AI-Powered Testing Capabilities
- **User Story**: As a development team, I want tests to adapt to UI changes automatically
- **Scope**: Test detects UI change, AI identifies new selector, test auto-heals
- **Verification**: Test passes after UI change with auto-heal notification

## Development Roadmap

### Current Phase: MVP Development
- ✅ Acceptance tests defined (4 scenarios)
- ✅ Test stubs created with NotImplementedError
- ⏳ Implement test creation functionality
- ⏳ Implement test execution engine
- ⏳ Integrate AI-powered self-healing capabilities

### Future Enhancements
- API endpoint testing support
- Mobile application testing
- Advanced visual regression testing
- Integration with CI/CD pipelines
- Multi-user collaboration features
- Test analytics dashboard

## Contributing

This project is part of CSC-510 coursework. For questions or contributions, please follow the course guidelines.

## License

Educational project for NC State University CSC-510.

---

**Last Updated**: January 2026
**Course**: CSC-510 Software Engineering
**Deliverable**: Acceptance Tests (Deliverable 1)
