"""Step definitions for Test Scenario Creation feature.

Deliverable 2 scope: implement ONLY Scenario 1 in
acceptance_tests/test_creation.feature.

Implementation approach:
- Use an in-memory platform prototype (testflow.platform.TestFlowPlatform)
  instead of a real UI so the acceptance test is deterministic and runnable
  in Docker.
"""

from behave import given, when, then

from testflow.platform import TestFlowPlatform


def _platform(context) -> TestFlowPlatform:
    """Get/create the shared platform instance for the current scenario."""
    if not hasattr(context, "platform"):
        context.platform = TestFlowPlatform()
    return context.platform


@given('I am logged into the testing platform')
def step_logged_in(context):
    _platform(context).login()


@when('I navigate to the "Create Test" page')
def step_navigate_to_create_test(context):
    _platform(context).navigate("Create Test")


@when('I enter the test name "{test_name}"')
def step_enter_test_name(context, test_name):
    context.test_state["test_name"] = test_name


@when('I enter the application URL "{url}"')
def step_enter_application_url(context, url):
    context.test_state["application_url"] = url


@when('I provide the test steps in natural language:')
def step_provide_nl_steps(context):
    # Behave stores the docstring in context.text
    context.test_state["nl_steps_raw"] = (context.text or "").strip()


@when('I set expected outcome "{outcome}"')
def step_set_expected_outcome(context, outcome):
    context.test_state["expected_outcome"] = outcome


@when('I click "Save Test"')
def step_save_test(context):
    created = _platform(context).create_test(
        name=context.test_state["test_name"],
        url=context.test_state["application_url"],
        nl_steps_raw=context.test_state["nl_steps_raw"],
        expected_outcome=context.test_state["expected_outcome"],
    )
    context.test_state["created_test"] = created


@then('I should see a confirmation message "{message}"')
def step_see_confirmation(context, message):
    assert _platform(context).last_confirmation_message == message


@then('the test should appear in my test list with status "{status}"')
def step_test_appears_in_list(context, status):
    tests = _platform(context).list_tests()
    name = context.test_state["test_name"]
    assert any(t.name == name and t.status == status for t in tests), (
        f"Expected test '{name}' with status '{status}'. Found: {[ (t.name, t.status) for t in tests ]}"
    )
