"""Unit tests for smart notification policy helpers."""

import src.notifications as notifications


def _failed_result(category="application_bug", message="Payment API timeout"):
    return {
        "status": "Failed",
        "failure_message": message,
        "diagnosis": {"category": category},
    }


def test_passed_result_does_not_trigger_notification():
    payload = notifications.process_smart_notification(
        {"name": "Checkout", "expected_outcome": "Order confirmation"},
        {"status": "Passed"},
        recipient="qa@example.com",
    )
    assert payload["notification_triggered"] is False


def test_application_bug_uses_report_email_and_simulated_delivery(monkeypatch):
    monkeypatch.delenv("TESTFLOW_SMTP_HOST", raising=False)
    payload = notifications.process_smart_notification(
        {"name": "Payment Processing", "application_url": "http://shop"},
        _failed_result(),
        recipient="qa-alerts@example.com",
    )
    assert payload["notification_recipient"] == "qa-alerts@example.com"
    assert payload["notification_triggered"] is True
    assert payload["notification_delivery"] == "simulated"
    assert payload["email_sent"] is True


def test_noncritical_test_design_failure_is_suppressed():
    payload = notifications.process_smart_notification(
        {"name": "Broken Button", "expected_outcome": "Element found"},
        _failed_result(category="test_design", message="Could not find element"),
        recipient="qa@example.com",
    )
    assert payload["notification_triggered"] is False
    assert payload["notification_delivery"] == "suppressed"


def test_timeout_failure_message_triggers_urgent_reason(monkeypatch):
    monkeypatch.delenv("TESTFLOW_SMTP_HOST", raising=False)
    payload = notifications.process_smart_notification(
        {"name": "Profile Update", "expected_outcome": "Profile saved"},
        _failed_result(category="test_design", message="504 timeout from target app"),
        recipient="qa@example.com",
    )
    assert "availability or latency" in payload["notification_reason"]


def test_smtp_success_reports_smtp_sent(monkeypatch):
    sent_messages = []

    class DummySMTP:
        def __init__(self, host, port, timeout):
            self.host = host
            self.port = port
            self.timeout = timeout

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def starttls(self):
            return None

        def login(self, username, password):
            return None

        def send_message(self, message):
            sent_messages.append(message)

    monkeypatch.setenv("TESTFLOW_SMTP_HOST", "smtp.example.com")
    monkeypatch.setenv("TESTFLOW_SMTP_PORT", "587")
    monkeypatch.setenv("TESTFLOW_SMTP_USERNAME", "sender@example.com")
    monkeypatch.setenv("TESTFLOW_SMTP_PASSWORD", "secret")
    monkeypatch.setenv("TESTFLOW_SMTP_FROM", "sender@example.com")
    monkeypatch.setattr(notifications.smtplib, "SMTP", DummySMTP)

    payload = notifications.process_smart_notification(
        {"name": "Payment Processing", "application_url": "http://shop"},
        _failed_result(),
        recipient="qa-alerts@example.com",
    )
    assert payload["notification_delivery"] == "smtp_sent"
    assert sent_messages[0]["To"] == "qa-alerts@example.com"


def test_smtp_error_falls_back_to_simulated(monkeypatch):
    class FailingSMTP:
        def __init__(self, host, port, timeout):
            pass

        def __enter__(self):
            raise OSError("SMTP unavailable")

        def __exit__(self, exc_type, exc, tb):
            return False

    monkeypatch.setenv("TESTFLOW_SMTP_HOST", "smtp.example.com")
    monkeypatch.setattr(notifications.smtplib, "SMTP", FailingSMTP)

    payload = notifications.process_smart_notification(
        {"name": "Login Production", "application_url": "http://app"},
        _failed_result(category="environment", message="Connection refused"),
        recipient="ops@example.com",
    )
    assert payload["notification_delivery"] == "simulated"
    assert "SMTP unavailable" in payload["notification_error"]
