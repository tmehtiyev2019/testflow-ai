# Quick Start Guide - Deliverable 1

## For Team Members & TAs

This is a quick reference guide for running and verifying the acceptance tests.

---

## 🚀 5-Minute Setup

### 1. Navigate to Project
```bash
cd testflow-ai
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Verify Installation
```bash
behave --version
# Expected output: behave 1.2.6
```

---

## ✅ Running Tests

### Run All Acceptance Tests
```bash
behave acceptance_tests/
```

**Expected Result**: All 4 scenarios should FAIL with `NotImplementedError`

### Run Individual Features
```bash
# Test Creation
behave acceptance_tests/test_creation.feature

# Test Execution
behave acceptance_tests/test_execution.feature

# AI Capabilities (SWAP CHALLENGE)
behave acceptance_tests/ai_capabilities.feature
```

### Run Specific Scenario
```bash
# Run just the SWAP CHALLENGE
behave acceptance_tests/ --name "SWAP CHALLENGE"

# Run with verbose output
behave acceptance_tests/ --verbose
```

---

## 📋 What You'll See

### Expected Output (All Tests Failing)
```
Feature: Test Scenario Creation

  Scenario: Create a simple web application test using natural language
    Given I am logged into the testing platform ... failed
    Traceback (most recent call last):
      ...
    NotImplementedError: Step not yet implemented

Feature: Test Execution and Monitoring

  Scenario: Execute a web application test and view results
    Given I have a saved test scenario "User Login Flow" ... failed
    NotImplementedError: Step not yet implemented

  Scenario: View detailed failure report when test fails
    Given I have a test scenario "Payment Processing" ... failed
    NotImplementedError: Step not yet implemented

Feature: AI-Powered Testing Capabilities

  Scenario: SWAP CHALLENGE - Self-healing test adapts to UI changes
    Given I have a test scenario "Add Product to Wishlist" ... failed
    NotImplementedError: Step not yet implemented

-----------------------------------
Failing scenarios:
  acceptance_tests/test_creation.feature:5  Create a simple web application test using natural language
  acceptance_tests/test_execution.feature:7  Execute a web application test and view results
  acceptance_tests/test_execution.feature:22  View detailed failure report when test fails
  acceptance_tests/ai_capabilities.feature:7  SWAP CHALLENGE - Self-healing test adapts to UI changes

0 features passed, 3 failed, 0 skipped
0 scenarios passed, 4 failed, 0 skipped
0 steps passed, 4 failed, 0 skipped, X undefined
```

---

## 📁 Project Structure

```
testflow-ai/
├── acceptance_tests/
│   ├── test_creation.feature       # Scenario 1: Test creation
│   ├── test_execution.feature      # Scenarios 2 & 3: Execution & reporting
│   ├── ai_capabilities.feature     # Scenario 4: SWAP CHALLENGE
│   ├── steps/                      # Step definitions (all raise NotImplementedError)
│   │   ├── test_creation_steps.py
│   │   ├── test_execution_steps.py
│   │   └── ai_capabilities_steps.py
│   └── environment.py              # Behave configuration
├── README.md                       # Main documentation
├── PRODUCT_SPECIFICATION.md        # Detailed product spec
├── QUICK_START.md                  # This file
└── requirements.txt                # Python dependencies
```

---

## 🎯 The 4 Scenarios

### Scenario 1: Test Creation
**Feature**: Create tests using natural language
**File**: `acceptance_tests/test_creation.feature:5`
**User Story**: QA engineer creates test without coding

### Scenario 2: Test Execution
**Feature**: Execute test and view results
**File**: `acceptance_tests/test_execution.feature:7`
**User Story**: Product manager runs test and sees pass/fail, screenshots

### Scenario 3: Failure Diagnosis
**Feature**: View detailed failure reports
**File**: `acceptance_tests/test_execution.feature:22`
**User Story**: Developer understands why test failed with AI diagnosis

### Scenario 4: SWAP CHALLENGE (Self-Healing)
**Feature**: Tests adapt to UI changes automatically
**File**: `acceptance_tests/ai_capabilities.feature:7`
**User Story**: Dev team reduces test maintenance with AI self-healing

---

## 🔍 Verification Checklist

- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Can run `behave --version` successfully
- [ ] Running `behave acceptance_tests/` shows 4 failing scenarios
- [ ] All failures are `NotImplementedError` exceptions
- [ ] Can run individual feature files
- [ ] Can run SWAP CHALLENGE scenario by name
- [ ] README.md exists with installation instructions
- [ ] All step definition files exist in `steps/` directory

---

## 🐛 Troubleshooting

### "behave: command not found"
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall behave
pip install behave
```

### "No steps directory found"
```bash
# Verify structure
ls -la acceptance_tests/steps/

# Should show:
# test_creation_steps.py
# test_execution_steps.py
# ai_capabilities_steps.py
```

### "Import errors"
```bash
# Reinstall all dependencies
pip install --force-reinstall -r requirements.txt
```

---

## 📚 Additional Resources

### Documentation Files
- **README.md**: Complete project documentation with setup instructions
- **PRODUCT_SPECIFICATION.md**: Detailed product vision, features, and architecture

### BDD Resources
- [Behave Documentation](https://behave.readthedocs.io/)
- [Gherkin Syntax Reference](https://cucumber.io/docs/gherkin/reference/)
- [BDD Best Practices](https://automationpanda.com/2017/01/30/bdd-101-writing-good-gherkin/)

---

## 💡 Tips for Next Steps (Deliverable 2)

After this deliverable is graded, you'll implement the actual functionality:

1. **Remove `NotImplementedError`** from step definitions
2. **Add test logic** (Selenium, API calls, assertions)
3. **Build the application** that the tests validate
4. **Make tests pass** by implementing features

Example transformation:
```python
# Deliverable 1 (current)
@given('I am logged into the testing platform')
def step_impl(context):
    raise NotImplementedError('Step not yet implemented')

# Deliverable 2 (next)
@given('I am logged into the testing platform')
def step_impl(context):
    context.browser = webdriver.Chrome()
    context.browser.get('http://localhost:3000/login')
    context.browser.find_element(By.ID, 'email').send_keys('test@example.com')
    context.browser.find_element(By.ID, 'password').send_keys('password123')
    context.browser.find_element(By.ID, 'login-btn').click()
    assert 'Dashboard' in context.browser.title
```

---

## 📞 Contact

For questions about this deliverable:
- Check README.md for detailed documentation
- Review PRODUCT_SPECIFICATION.md for feature context
- Refer to assignment requirements in course materials

---

**Last Updated**: January 23, 2026
**Deliverable**: 1 - Acceptance Tests
**Status**: Ready for Submission ✅
