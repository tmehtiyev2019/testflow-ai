"""
Behave environment configuration for Black-Box E2E Testing SaaS
This file contains hooks that run before/after scenarios and features
"""


def before_all(context):
    """
    Setup hook that runs before all tests
    Initialize test configuration, database connections, etc.
    """
    print("\n=== Initializing Test Environment ===")
    context.config.setup_logging()


def before_feature(context, feature):
    """
    Setup hook that runs before each feature
    """
    print(f"\n--- Starting Feature: {feature.name} ---")


def before_scenario(context, scenario):
    """
    Setup hook that runs before each scenario
    Initialize browser, API clients, test data, etc.
    """
    print(f"\nStarting Scenario: {scenario.name}")
    # Initialize test state
    context.test_state = {}


def after_scenario(context, scenario):
    """
    Cleanup hook that runs after each scenario
    Close browser sessions, cleanup test data, etc.
    """
    if scenario.status == "failed":
        print(f"\n❌ Scenario FAILED: {scenario.name}")
    else:
        print(f"\n✅ Scenario PASSED: {scenario.name}")

    # Cleanup test state
    if hasattr(context, 'test_state'):
        context.test_state.clear()


def after_feature(context, feature):
    """
    Cleanup hook that runs after each feature
    """
    print(f"\n--- Completed Feature: {feature.name} ---")


def after_all(context):
    """
    Cleanup hook that runs after all tests
    """
    print("\n=== Test Execution Complete ===")
