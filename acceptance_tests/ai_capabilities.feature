Feature: Smart Notifications with Report Email
  As a QA lead
  I want failed critical workflows to notify my configured report email
  So that my team can respond quickly when important user journeys break

  Scenario: Report email receives a smart notification for a critical failure
    Given I am logged into the platform for smart notifications
    And I save report email "qa-alerts@example.com"
    And I have a critical failing notification test "Payment Processing Alert" with expected outcome "Payment confirmation message"
    When I run the critical failing notification test
    Then I should see test status as "Failed"
    And I should see a smart notification sent to "qa-alerts@example.com"
    And I should see smart notification reason "Application bug detected in a monitored workflow."
    And I should see smart notification delivery "Logged as a simulated alert because SMTP delivery failed"
    And the notification should be stored with recipient "qa-alerts@example.com"
