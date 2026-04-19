"""Integration coverage for Scenario 4: Report Email smart notifications."""

import pytest

from src.app import create_app
from src import db as db_module


@pytest.fixture(autouse=True)
def _scenario4_env(tmp_path, monkeypatch):
    db_file = str(tmp_path / "scenario4.db")
    monkeypatch.setattr(db_module, "DB_PATH", db_file)
    monkeypatch.setenv("TESTFLOW_SIMULATE", "1")
    monkeypatch.delenv("TESTFLOW_SMTP_HOST", raising=False)


@pytest.fixture()
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def _login(client):
    return client.post("/login", data={
        "email": "test@example.com",
        "password": "password123",
    }, follow_redirects=True)


def _create_test(client, name, outcome):
    return client.post("/create-test", data={
        "test_name": name,
        "application_url": "http://shop.example.com",
        "steps_raw": "Navigate to checkout\nClick Pay Now\nVerify confirmation",
        "expected_outcome": outcome,
    }, follow_redirects=True)


def test_report_email_is_used_for_critical_failure_notification(client):
    _login(client)
    client.post("/settings", data={
        "action": "save_settings",
        "report_email": "qa-alerts@example.com",
    }, follow_redirects=True)
    _create_test(client, "Payment Processing Alert", "Payment confirmation message")
    test = db_module.get_all_tests()[0]

    response = client.post(f"/run-test/{test['id']}", follow_redirects=True)
    run = db_module.get_latest_test_run(test["id"])

    assert response.status_code == 200
    assert b"Smart notification triggered for qa-alerts@example.com" in response.data
    assert run["notification_recipient"] == "qa-alerts@example.com"
    assert run["notification_triggered"] == 1
    assert run["notification_delivery"] == "simulated"


def test_report_email_notification_reason_is_stored(client):
    _login(client)
    client.post("/settings", data={
        "action": "save_settings",
        "report_email": "qa-alerts@example.com",
    }, follow_redirects=True)
    _create_test(client, "Payment Processing Alert", "Payment confirmation message")
    test = db_module.get_all_tests()[0]

    client.post(f"/run-test/{test['id']}", follow_redirects=True)
    run = db_module.get_latest_test_run(test["id"])

    assert run["notification_reason"] == "Application bug detected in a monitored workflow."


def test_missing_report_email_falls_back_to_logged_in_user(client):
    _login(client)
    _create_test(client, "Payment Processing Alert", "Payment confirmation message")
    test = db_module.get_all_tests()[0]

    client.post(f"/run-test/{test['id']}", follow_redirects=True)
    run = db_module.get_latest_test_run(test["id"])

    assert run["notification_recipient"] == "test@example.com"


def test_noncritical_test_design_failure_is_suppressed_in_workflow(client):
    _login(client)
    client.post("/settings", data={
        "action": "save_settings",
        "report_email": "qa-alerts@example.com",
    }, follow_redirects=True)
    _create_test(client, "Broken Selector", "element not found on page")
    test = db_module.get_all_tests()[0]

    response = client.post(f"/run-test/{test['id']}", follow_redirects=True)
    run = db_module.get_latest_test_run(test["id"])

    assert b"No notification was sent" in response.data
    assert run["notification_triggered"] == 0
    assert run["notification_delivery"] == "suppressed"
