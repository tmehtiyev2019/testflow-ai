"""Flask web application for Scenario 1 (Test Creation).

This module implements the web UI that the Scenario 1 acceptance test drives
via Selenium. The full Scenario 1 flow through these routes is:

    1. GET  /login       → user sees login form       (step: "I am logged into the testing platform")
    2. POST /login       → authenticate, redirect      (step: "I am logged into the testing platform")
    3. GET  /create-test → user sees creation form     (step: "I navigate to the Create Test page")
    4. POST /create-test → save test, flash message    (step: "I click Save Test")
    5. GET  /tests       → user sees test in list      (step: "test should appear in my test list")
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash

from src.db import init_db, insert_test, get_all_tests

# Hardcoded credentials for the prototype.
# Scenario 1: used by the "I am logged into the testing platform" step.
VALID_EMAIL = "test@example.com"
VALID_PASSWORD = "password123"


def create_app() -> Flask:
    """Application factory — creates and configures the Flask app.

    Called by environment.py before_all() to start the server for acceptance tests,
    or directly to run the app standalone for manual testing.
    """
    app = Flask(__name__)
    app.secret_key = "testflow-dev-secret-key"

    # Ensure the database table exists on startup.
    with app.app_context():
        init_db()

    # --- Scenario 1, step: "Given I am logged into the testing platform" ---
    # Selenium navigates here, fills email/password, and submits the form.

    @app.route("/login", methods=["GET", "POST"])
    def login():
        """Scenario 1: login route.

        GET  — render the login form (email + password fields).
        POST — validate credentials, set session, redirect to test list.
        """
        if request.method == "POST":
            email = request.form.get("email", "")
            password = request.form.get("password", "")
            if email == VALID_EMAIL and password == VALID_PASSWORD:
                session["logged_in"] = True
                return redirect(url_for("test_list"))
            flash("Invalid credentials", "error")
        return render_template("login.html")

    # --- Scenario 1, steps: form input + "When I click Save Test" ---
    # Selenium fills the form fields and clicks the save button.

    @app.route("/create-test", methods=["GET", "POST"])
    def create_test():
        """Scenario 1: test creation route.

        GET  — render the creation form (test_name, application_url,
               steps_raw textarea, expected_outcome).
        POST — insert test into SQLite via insert_test(), flash the
               confirmation message, and redirect to /tests.
               The flash message "Test scenario created successfully" is
               verified by the step: 'I should see a confirmation message "..."'.
        """
        if not session.get("logged_in"):
            return redirect(url_for("login"))

        if request.method == "POST":
            name = request.form.get("test_name", "")
            application_url = request.form.get("application_url", "")
            steps_raw = request.form.get("steps_raw", "")
            expected_outcome = request.form.get("expected_outcome", "")

            insert_test(name, application_url, steps_raw, expected_outcome)
            flash("Test scenario created successfully", "success")
            return redirect(url_for("test_list"))

        return render_template("create_test.html")

    # --- Scenario 1, step: "the test should appear in my test list with status" ---
    # After saving, Selenium is redirected here and checks the table.

    @app.route("/tests")
    def test_list():
        """Scenario 1: test list route.

        Queries all saved tests from SQLite and renders them in an HTML table.
        Each row shows the test name (class="test-name") and status (class="test-status").
        Selenium verifies the test name and "Not Run" status appear in this table.
        """
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        tests = get_all_tests()
        return render_template("test_list.html", tests=tests)

    @app.route("/")
    def index():
        """Redirect root URL to login page."""
        return redirect(url_for("login"))

    return app
