"""Step definitions for Scenario 4: Smart Notifications with Report Email."""

from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.db import get_latest_test_run, get_setting, insert_test


def _login(context):
    """Log in through the browser so Scenario 4 exercises the real UI session."""
    context.driver.get(f"{context.base_url}/login")
    context.driver.find_element(By.ID, "email").send_keys("test@example.com")
    context.driver.find_element(By.ID, "password").send_keys("password123")
    context.driver.find_element(By.ID, "login-btn").click()
    WebDriverWait(context.driver, 5).until(lambda d: "/login" not in d.current_url)


@given("I am logged into the platform for smart notifications")
def step_logged_in_for_notifications(context):
    """Authenticate as the seeded user before configuring notification settings."""
    _login(context)


@given('I save report email "{email}"')
def step_save_report_email(context, email):
    """Save the Report Email through the Settings page and verify persistence."""
    context.driver.get(f"{context.base_url}/settings")
    email_input = WebDriverWait(context.driver, 5).until(
        EC.presence_of_element_located((By.ID, "report_email"))
    )
    email_input.clear()
    email_input.send_keys(email)
    if email_input.get_attribute("value") != email:
        context.driver.execute_script(
            "arguments[0].value = arguments[1];"
            "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
            email_input,
            email,
        )
    form = email_input.find_element(By.XPATH, "./ancestor::form")
    form.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    WebDriverWait(context.driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "flash-success"))
    )
    saved = get_setting("report_email")
    assert saved == email, f"Expected report email '{email}', got '{saved}'"
    context.test_state["report_email"] = email


@given('I have a critical failing notification test "{test_name}" with expected outcome "{expected_outcome}"')
def step_have_critical_failing_notification_test(context, test_name, expected_outcome):
    """Create a payment failure scenario that should trigger smart notification rules."""
    test_id = insert_test(
        name=test_name,
        application_url="http://localhost:5000",
        steps_raw=(
            "1. Navigate to /checkout\n"
            "2. Enter card number\n"
            "3. Click Pay Now\n"
            "4. Verify payment confirmation"
        ),
        expected_outcome=expected_outcome,
    )
    context.test_state["test_id"] = test_id
    context.test_state["test_name"] = test_name


@when("I run the critical failing notification test")
def step_run_critical_failing_notification_test(context):
    """Run the seeded critical test through the list page."""
    test_name = context.test_state["test_name"]
    context.driver.get(f"{context.base_url}/tests")
    WebDriverWait(context.driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "test-name"))
    )

    rows = context.driver.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        name_cells = row.find_elements(By.CLASS_NAME, "test-name")
        if name_cells and name_cells[0].text == test_name:
            row.find_element(By.CLASS_NAME, "run-test-btn").click()
            break
    else:
        raise AssertionError(f"Test '{test_name}' not found in test list")

    WebDriverWait(context.driver, 30).until(
        lambda d: "/test-results/" in d.current_url
    )
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "test-run-status"))
    )


@then('I should see a smart notification sent to "{email}"')
def step_see_smart_notification_recipient(context, email):
    """Verify the results page shows the configured report email recipient."""
    notification = context.driver.find_element(By.CLASS_NAME, "email-sent-text")
    actual = notification.text.strip()
    assert email in actual, f"Expected notification recipient '{email}', got '{actual}'"


@then('I should see smart notification reason "{reason}"')
def step_see_smart_notification_reason(context, reason):
    """Verify the trigger reason is visible on the results page."""
    page_source = context.driver.page_source
    assert reason in page_source, f"Expected notification reason '{reason}'"


@then('I should see smart notification delivery "{delivery}"')
def step_see_smart_notification_delivery(context, delivery):
    """Verify deterministic simulated delivery is shown when SMTP is not configured."""
    page_source = context.driver.page_source
    assert delivery in page_source, f"Expected notification delivery '{delivery}'"


@then('the notification should be stored with recipient "{email}"')
def step_notification_stored_with_recipient(context, email):
    """Verify the notification metadata is persisted with the test run."""
    run = get_latest_test_run(context.test_state["test_id"])
    assert run is not None, "Expected a stored test run"
    assert run["notification_triggered"] == 1, "Expected notification to be triggered"
    assert run["notification_recipient"] == email, (
        f"Expected stored recipient '{email}', got '{run['notification_recipient']}'"
    )
