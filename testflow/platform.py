"""In-memory platform prototype for Deliverable 2 (Scenario 1: Test Creation)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class TestScenario:
    """Saved test scenario (used by Scenario 1 acceptance test)."""

    name: str
    application_url: str
    natural_language_steps_raw: str
    expected_outcome: str

    # Scenario 1 requires this default status in the list view.
    status: str = "Not Run"

    # Convenience: parsed list of steps from the natural-language input.
    steps: List[str] = field(default_factory=list)


class TestFlowPlatform:
    """Tiny in-memory "platform" used by Behave step definitions.

    Scenario mapping:
    - Scenario 1: login -> navigate -> enter fields -> save -> confirmation -> appears in list
    """

    def __init__(self) -> None:
        self.logged_in: bool = False
        self.current_page: str = "Unknown"
        self._tests: List[TestScenario] = []
        self.last_confirmation_message: Optional[str] = None

    # --- Scenario 1: authentication / navigation ---
    def login(self) -> None:
        self.logged_in = True
        self.current_page = "Home"

    def navigate(self, page_name: str) -> None:
        if not self.logged_in:
            raise RuntimeError("User must be logged in before navigation")
        self.current_page = page_name

    # --- Scenario 1: create / list tests ---
    def create_test(self, *, name: str, url: str, nl_steps_raw: str, expected_outcome: str) -> TestScenario:
        if not self.logged_in:
            raise RuntimeError("User must be logged in to create tests")
        if self.current_page != "Create Test":
            raise RuntimeError("User must be on 'Create Test' page")

        scenario = TestScenario(
            name=name,
            application_url=url,
            natural_language_steps_raw=nl_steps_raw.strip(),
            expected_outcome=expected_outcome.strip(),
        )
        scenario.steps = self._parse_natural_language_steps(scenario.natural_language_steps_raw)

        self._tests.append(scenario)
        self.last_confirmation_message = "Test scenario created successfully"
        return scenario

    def list_tests(self) -> List[TestScenario]:
        return list(self._tests)

    @staticmethod
    def _parse_natural_language_steps(nl: str) -> List[str]:
        """Prototype parser: one step per non-empty line; strips leading '1.'/'2)' etc."""
        steps: List[str] = []
        for raw in nl.splitlines():
            line = raw.strip()
            if not line:
                continue
            if len(line) >= 2 and line[0].isdigit() and line[1] in {".", ")"}:
                line = line[2:].strip()
            steps.append(line)
        return steps
