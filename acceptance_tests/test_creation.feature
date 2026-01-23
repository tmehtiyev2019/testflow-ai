Feature: Test Scenario Creation
  As a QA engineer
  I want to create test scenarios in natural language
  So that I can validate user workflows without writing code

  Scenario: Create a simple web application test using natural language
    Given I am logged into the testing platform
    When I navigate to the "Create Test" page
    And I enter the test name "Checkout Flow Validation"
    And I enter the application URL "https://example-shop.com"
    And I provide the test steps in natural language:
      """
      1. Navigate to homepage
      2. Click "Products" menu
      3. Select first product
      4. Click "Add to Cart"
      5. Verify cart shows 1 item
      """
    And I set expected outcome "Cart displays 1 item successfully"
    And I click "Save Test"
    Then I should see a confirmation message "Test scenario created successfully"
    And the test should appear in my test list with status "Not Run"
