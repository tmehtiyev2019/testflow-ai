"""Step definitions for Scenario 2: Test Execution and Monitoring.

Uses Selenium to drive a real headless Chromium browser against the Flask app.
Scenario 2 has two sub-scenarios:
    2A — Execute a test and verify pass results (status, time, screenshots, metrics).
    2B — Execute a failing test and verify failure report (message, diagnosis, email).

The steps pre-seed test data directly into the database, then use the web UI
to run the test and verify results on the results page.
"""

from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.db import insert_test, get_test_by_id


# ---------------------------------------------------------------------------
# Scenario 2A: Given steps — set up a saved test scenario
# ---------------------------------------------------------------------------

@given('I have a saved test scenario "{test_name}"')
def step_have_saved_test(context, test_name):
    """Scenario 2A: pre-seed a test scenario in the database.

    Inserts a test with default steps and expected outcome so the test list
    page shows it with a "Run Test" button.  Logs in via Selenium so the
    session is active for subsequent steps.
    """
    # Default steps for the "User Login Flow" test (Scenario 2A)
    test_id = insert_test(
        name=test_name,
        application_url="http://localhost:5000",
        steps_raw="1. Navigate to /login\n2. Enter email\n3. Enter password\n4. Click Sign In",
        expected_outcome="Dashboard page appears",
    )
    context.test_state["test_name"] = test_name
    context.test_state["test_id"] = test_id

    # Log in so we have an active session for the web UI
    context.driver.get(f"{context.base_url}/login")
    context.driver.find_element(By.ID, "email").send_keys("test@example.com")
    context.driver.find_element(By.ID, "password").send_keys("password123")
    context.driver.find_element(By.ID, "login-btn").click()
    WebDriverWait(context.driver, 5).until(lambda d: "/login" not in d.current_url)


@given('the test contains the following steps:')
def step_test_contains_steps(context):
    """Scenario 2A: store the data-table steps in context for later verification.

    The feature file defines steps as a Behave table; we save them here.
    The actual test record already has steps from the Given step above.
    """
    context.test_state["steps_table"] = context.table


# ---------------------------------------------------------------------------
# Scenario 2A: When steps — run the test
# ---------------------------------------------------------------------------

@when('I click "Run Test" for "{test_name}"')
def step_click_run_test(context, test_name):
    """Scenario 2A: navigate to test list and click the Run Test button.

    Finds the row matching the test name and clicks its Run Test button.
    """
    context.driver.get(f"{context.base_url}/tests")
    WebDriverWait(context.driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "test-name"))
    )

    # Find the Run Test button in the same row as the test name
    rows = context.driver.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        name_cells = row.find_elements(By.CLASS_NAME, "test-name")
        if name_cells and name_cells[0].text == test_name:
            run_btn = row.find_element(By.CLASS_NAME, "run-test-btn")
            run_btn.click()
            break
    else:
        raise AssertionError(f"Test '{test_name}' not found in test list")


@when('I wait for test execution to complete')
def step_wait_for_execution(context):
    """Scenario 2A: wait until we are redirected to the test results page.

    After clicking Run Test, the server simulates execution and redirects
    to /test-results/<id>. We wait for the results page to load.
    """
    WebDriverWait(context.driver, 10).until(
        lambda d: "/test-results/" in d.current_url
    )
    # Wait for the status badge to appear on the results page
    WebDriverWait(context.driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "test-run-status"))
    )


# ---------------------------------------------------------------------------
# Scenario 2A: Then steps — verify pass results
# ---------------------------------------------------------------------------

@then('I should see test status as "{status}"')
def step_see_test_status(context, status):
    """Scenario 2A/2B: verify the test run status displayed on results page.

    Checks the status badge text matches the expected value ("Passed" or "Failed").
    """
    status_el = context.driver.find_element(By.CLASS_NAME, "test-run-status")
    actual = status_el.text.strip()
    assert actual == status, f"Expected status '{status}', got '{actual}'"


@then('I should see execution time in seconds')
def step_see_execution_time(context):
    """Scenario 2A: verify execution time is displayed on results page.

    Checks that an element with class 'execution-time' exists and contains
    a numeric value followed by 's'.
    """
    time_el = context.driver.find_element(By.CLASS_NAME, "execution-time")
    text = time_el.text.strip()
    assert text.endswith("s"), f"Expected execution time ending with 's', got '{text}'"
    # Verify the numeric part is a valid float
    numeric = text.rstrip("s")
    float(numeric)  # Raises ValueError if not a number


@then('I should see screenshots for each step')
def step_see_screenshots(context):
    """Scenario 2A: verify screenshot placeholders are shown for each step.

    Checks that the screenshots section contains at least one screenshot item.
    """
    screenshots = context.driver.find_elements(By.CLASS_NAME, "screenshot-item")
    assert len(screenshots) > 0, "No screenshots found on results page"


@then('I should see performance metrics showing page load times')
def step_see_performance_metrics(context):
    """Scenario 2A: verify performance metrics table is displayed.

    Checks that metric values (page load times) are present in the table.
    """
    metrics = context.driver.find_elements(By.CLASS_NAME, "metric-value")
    assert len(metrics) > 0, "No performance metrics found on results page"
    # Verify each metric is a valid time value
    for m in metrics:
        text = m.text.strip()
        assert text.endswith("s"), f"Expected metric ending with 's', got '{text}'"


# ---------------------------------------------------------------------------
# Scenario 2B: Given steps — set up a failing test scenario
# ---------------------------------------------------------------------------

@given('I have a test scenario "{test_name}"')
def step_have_test_scenario(context, test_name):
    """Scenario 2B: pre-seed a test scenario configured to fail.

    The expected_outcome contains "Payment confirmation" which triggers
    the simulated failure path in the /run-test route.
    """
    test_id = insert_test(
        name=test_name,
        application_url="http://localhost:5000",
        steps_raw=(
            "1. Navigate to /checkout\n"
            "2. Enter card number\n"
            "3. Enter expiry date\n"
            "4. Enter CVV\n"
            "5. Click Pay Now\n"
            "6. Wait for processing\n"
            "7. Verify confirmation"
        ),
        expected_outcome="Payment confirmation message",
    )
    context.test_state["test_name"] = test_name
    context.test_state["test_id"] = test_id

    # Log in so we have an active session
    context.driver.get(f"{context.base_url}/login")
    context.driver.find_element(By.ID, "email").send_keys("test@example.com")
    context.driver.find_element(By.ID, "password").send_keys("password123")
    context.driver.find_element(By.ID, "login-btn").click()
    WebDriverWait(context.driver, 5).until(lambda d: "/login" not in d.current_url)


@given('the test is configured to verify "{verification_point}"')
def step_configured_to_verify(context, verification_point):
    """Scenario 2B: store the verification point in context.

    The test is already configured with the appropriate expected_outcome
    from the previous Given step; this step just records the verification point.
    """
    context.test_state["verification_point"] = verification_point


# ---------------------------------------------------------------------------
# Scenario 2B: When steps — execute and simulate failure
# ---------------------------------------------------------------------------

@when('I execute the test')
def step_execute_test(context):
    """Scenario 2B: navigate to test list and click Run Test for the current test.

    Uses the test name stored in context from the Given step.
    """
    test_name = context.test_state["test_name"]
    context.driver.get(f"{context.base_url}/tests")
    WebDriverWait(context.driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "test-name"))
    )

    rows = context.driver.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        name_cells = row.find_elements(By.CLASS_NAME, "test-name")
        if name_cells and name_cells[0].text == test_name:
            run_btn = row.find_element(By.CLASS_NAME, "run-test-btn")
            run_btn.click()
            break
    else:
        raise AssertionError(f"Test '{test_name}' not found in test list")

    # Wait for results page to load
    WebDriverWait(context.driver, 10).until(
        lambda d: "/test-results/" in d.current_url
    )
    WebDriverWait(context.driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "test-run-status"))
    )


@when('the payment API returns a timeout error')
def step_payment_timeout(context):
    """Scenario 2B: this is a simulated condition.

    The failure is already triggered by the expected_outcome containing
    "Payment confirmation" in the test data. This step verifies we are
    on the results page with a failure status.
    """
    # Already on the results page — the failure was simulated server-side.
    # Just verify the page loaded correctly.
    WebDriverWait(context.driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "test-run-status"))
    )


# ---------------------------------------------------------------------------
# Scenario 2B: Then steps — verify failure report
# ---------------------------------------------------------------------------

@then('I should see failure message "{message}"')
def step_see_failure_message(context, message):
    """Scenario 2B: verify the failure message is displayed on results page.

    Checks that the failure text element contains the expected error message.
    """
    failure_el = context.driver.find_element(By.CLASS_NAME, "failure-text")
    actual = failure_el.text.strip()
    assert message in actual, f"Expected failure message '{message}', got '{actual}'"


@then('I should see a screenshot of the failure point')
def step_see_failure_screenshot(context):
    """Scenario 2B: verify a failure screenshot is shown on results page.

    Checks that the screenshots section includes a failure_point screenshot.
    """
    page_source = context.driver.page_source
    assert "failure_point" in page_source, "Failure point screenshot not found on page"


@then('I should see AI-powered diagnosis suggesting "{suggestion}"')
def step_see_ai_diagnosis(context, suggestion):
    """Scenario 2B: verify AI diagnosis text is displayed on results page.

    Checks the diagnosis section contains the expected suggestion text.
    """
    diagnosis_el = context.driver.find_element(By.CLASS_NAME, "diagnosis-text")
    actual = diagnosis_el.text.strip()
    assert suggestion in actual, f"Expected diagnosis '{suggestion}', got '{actual}'"


@then('I should receive an email notification about the failure')
def step_receive_email_notification(context):
    """Scenario 2B: verify email notification indicator is shown.

    In this prototype, email sending is simulated. The results page
    displays a message confirming that a notification was sent.
    """
    email_el = context.driver.find_element(By.CLASS_NAME, "email-sent-text")
    actual = email_el.text.strip()
    assert "notification" in actual.lower() or "email" in actual.lower(), \
        f"Expected email notification message, got '{actual}'"
