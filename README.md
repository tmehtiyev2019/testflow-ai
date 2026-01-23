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
- **Python**: 3.8 or higher
- **pip**: Latest version
- **Operating System**: macOS, Linux, or Windows with WSL2

### Required Python Packages

```bash
behave>=1.2.6
selenium>=4.0.0
requests>=2.28.0
pytest>=7.0.0
```

### Optional Dependencies (for enhanced features)
```bash
allure-behave>=2.13.0  # For advanced reporting
python-dotenv>=1.0.0   # For environment configuration
```

### Browser Requirements (for web testing)
- Chrome/Chromium (recommended)
- ChromeDriver (matching your Chrome version)
- Firefox (optional, for multi-browser testing)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd project
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation**:
   ```bash
   behave --version
   ```

## Project Structure

```
project/
├── acceptance_tests/
│   ├── test_creation.feature          # Test scenario creation feature
│   ├── test_execution.feature         # Test execution and monitoring feature
│   ├── ai_capabilities.feature        # AI-powered testing (SWAP CHALLENGE)
│   ├── steps/
│   │   ├── test_creation_steps.py     # Step definitions for test creation
│   │   ├── test_execution_steps.py    # Step definitions for execution
│   │   └── ai_capabilities_steps.py   # Step definitions for AI features
│   └── environment.py                 # Behave test environment configuration
├── README.md                          # This file
└── requirements.txt                   # Python dependencies
```

## Instructions to Run Acceptance Tests

### Prerequisites Check

Before running tests, ensure your environment is properly configured:

```bash
# Verify Python version (should be 3.8+)
python --version

# Verify Behave is installed
behave --version

# Activate virtual environment if not already active
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Running All Acceptance Tests

To run all acceptance tests in the project:

```bash
behave acceptance_tests/
```

**Expected Output**: All tests should initially **FAIL** with `NotImplementedError` exceptions, as the step implementations are stubs.

### Running Specific Feature Files

To run tests for a specific feature:

```bash
# Test Creation feature
behave acceptance_tests/test_creation.feature

# Test Execution feature
behave acceptance_tests/test_execution.feature

# AI Capabilities feature (includes SWAP CHALLENGE)
behave acceptance_tests/ai_capabilities.feature
```

### Running Specific Scenarios

To run a specific scenario by name:

```bash
behave acceptance_tests/ --name "Create a simple web application test using natural language"

# Run the SWAP CHALLENGE scenario
behave acceptance_tests/ --name "SWAP CHALLENGE"
```

### Running with Verbose Output

For detailed step-by-step output:

```bash
behave acceptance_tests/ --verbose
```

### Running with Tags (Future Enhancement)

Once tags are added to scenarios, you can filter tests:

```bash
# Run only tests tagged with @critical
behave acceptance_tests/ --tags=@critical

# Skip tests tagged with @wip (work in progress)
behave acceptance_tests/ --tags=~@wip
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
behave acceptance_tests/ -f allure_behave.formatter:AllureFormatter -o ./reports

# Generate and view HTML report
allure serve ./reports
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
