"""Behave environment configuration.

Starts a real Flask server and headless Chromium browser for Scenario 1.
- before_all:  launch Flask in a background thread, create Selenium driver.
- before_scenario: reset the database for a clean state.
- after_all:   quit Selenium driver, stop Flask server.
"""

import threading
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from src.app import create_app
from src.db import reset_db

# Flask server settings
FLASK_HOST = "127.0.0.1"
FLASK_PORT = 5000
BASE_URL = f"http://{FLASK_HOST}:{FLASK_PORT}"


def before_all(context):
    """Start Flask app and Selenium browser."""
    print("\n=== Initializing Test Environment ===")
    context.config.setup_logging()

    # --- Start Flask in a background thread ---
    app = create_app()
    context.flask_app = app
    context.server_thread = threading.Thread(
        target=app.run,
        kwargs={"host": FLASK_HOST, "port": FLASK_PORT, "use_reloader": False},
        daemon=True,
    )
    context.server_thread.start()
    # Give Flask a moment to start.
    time.sleep(1)

    # --- Start headless Chromium via Selenium ---
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.binary_location = "/usr/bin/chromium"

    service = Service("/usr/bin/chromedriver")
    context.driver = webdriver.Chrome(service=service, options=chrome_options)
    context.base_url = BASE_URL

    print(f"Flask running at {BASE_URL}")
    print("Selenium headless Chromium ready")


def before_feature(context, feature):
    print(f"\n--- Starting Feature: {feature.name} ---")


def before_scenario(context, scenario):
    print(f"\nStarting Scenario: {scenario.name}")
    # Clean database before each scenario.
    reset_db()
    # Shared scratch space for step definitions.
    context.test_state = {}


def after_scenario(context, scenario):
    status_str = str(getattr(scenario, "status", "unknown")).lower()
    if "passed" in status_str:
        print(f"\n  Scenario PASSED: {scenario.name}")
    else:
        print(f"\n  Scenario {status_str.upper()}: {scenario.name}")
    if hasattr(context, "test_state"):
        context.test_state.clear()


def after_feature(context, feature):
    print(f"\n--- Completed Feature: {feature.name} ---")


def after_all(context):
    """Shut down Selenium and Flask."""
    if hasattr(context, "driver"):
        context.driver.quit()
        print("Selenium driver closed")
    print("\n=== Test Execution Complete ===")
