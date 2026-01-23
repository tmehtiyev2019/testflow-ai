Feature: Test Execution and Monitoring
  As a product manager
  I want to execute tests and monitor their results
  So that I can ensure critical user journeys work correctly

  Scenario: Execute a web application test and view results
    Given I have a saved test scenario "User Login Flow"
    And the test contains the following steps:
      | Step | Action                          | Expected Result           |
      | 1    | Navigate to /login              | Login page loads          |
      | 2    | Enter email "test@example.com"  | Email field populated     |
      | 3    | Enter password "securePass123"  | Password field populated  |
      | 4    | Click "Sign In" button          | Dashboard page appears    |
    When I click "Run Test" for "User Login Flow"
    And I wait for test execution to complete
    Then I should see test status as "Passed"
    And I should see execution time in seconds
    And I should see screenshots for each step
    And I should see performance metrics showing page load times

  Scenario: View detailed failure report when test fails
    Given I have a test scenario "Payment Processing"
    And the test is configured to verify "Payment confirmation message"
    When I execute the test
    And the payment API returns a timeout error
    Then I should see test status as "Failed"
    And I should see failure message "Payment API timeout at step 7"
    And I should see a screenshot of the failure point
    And I should see AI-powered diagnosis suggesting "Payment gateway may be down or experiencing high latency"
    And I should receive an email notification about the failure
