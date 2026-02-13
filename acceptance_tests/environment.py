"""Behave environment configuration.

Note: Deliverable 2 focuses on Scenario 1 (test_creation.feature).
These hooks keep output readable and initialize per-scenario state.
"""


def before_all(context):
    print("\n=== Initializing Test Environment ===")
    context.config.setup_logging()


def before_feature(context, feature):
    print(f"\n--- Starting Feature: {feature.name} ---")


def before_scenario(context, scenario):
    print(f"\nStarting Scenario: {scenario.name}")
    # Shared scratch space for step definitions
    context.test_state = {}


def after_scenario(context, scenario):
    # Behave may represent status as an enum (e.g., Status.passed) depending on version.
    status_str = str(getattr(scenario, "status", "unknown")).lower()

    if "passed" in status_str:
        print(f"\n✅ Scenario PASSED: {scenario.name}")
    else:
        # Covers "failed", "error", "skipped", etc.
        print(f"\n❌ Scenario {status_str.upper()}: {scenario.name}")

    if hasattr(context, "test_state"):
        context.test_state.clear()


def after_feature(context, feature):
    print(f"\n--- Completed Feature: {feature.name} ---")


def after_all(context):
    print("\n=== Test Execution Complete ===")
