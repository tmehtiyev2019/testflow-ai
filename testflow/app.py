"""Flask web application for Scenario 1 (Test Creation).

Routes:
    GET  /login       — Show login form.
    POST /login       — Authenticate user (hardcoded credentials for prototype).
    GET  /create-test — Show the test creation form (requires login).
    POST /create-test — Save a new test scenario to SQLite, redirect to test list.
    GET  /tests       — List all saved test scenarios with name and status.
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash

from testflow.db import init_db, insert_test, get_all_tests

# Hardcoded credentials for the prototype (Scenario 1).
VALID_EMAIL = "test@example.com"
VALID_PASSWORD = "password123"


def create_app() -> Flask:
    """Application factory — creates and configures the Flask app."""
    app = Flask(__name__)
    app.secret_key = "testflow-dev-secret-key"

    # Ensure DB table exists on startup.
    with app.app_context():
        init_db()

    # --- Scenario 1: Login ---

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form.get("email", "")
            password = request.form.get("password", "")
            if email == VALID_EMAIL and password == VALID_PASSWORD:
                session["logged_in"] = True
                return redirect(url_for("test_list"))
            flash("Invalid credentials", "error")
        return render_template("login.html")

    # --- Scenario 1: Create Test ---

    @app.route("/create-test", methods=["GET", "POST"])
    def create_test():
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

    # --- Scenario 1: Test List ---

    @app.route("/tests")
    def test_list():
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        tests = get_all_tests()
        return render_template("test_list.html", tests=tests)

    # Redirect root to login.
    @app.route("/")
    def index():
        return redirect(url_for("login"))

    return app
