# Example Test Inputs

## Example 1: Kanboard Login & Create Project

| Field             | Value                                                  |
|-------------------|--------------------------------------------------------|
| **Test Name**     | Kanboard Login & Create Project                        |
| **Application URL** | http://localhost:8080                                |
| **Test Steps**    | Enter admin in username                                |
|                   | Enter admin in password                                |
|                   | Click Sign In                                          |
|                   | Click New project                                      |
|                   | Enter Demo Project in name                             |
|                   | Click Save                                             |
| **Expected Outcome** | Demo Project                                        |

## How to Run

1. Open http://localhost:5001 in your browser
2. Login with `test@example.com` / `password123` (or register a new account)
3. Click **Create Test** and fill in the fields from the table above
4. Click **Save Test**
5. Click **Run Test** — it will execute against the real Kanboard instance and show real screenshots, real timing, real pass/fail

## What Happens During Execution

| Aspect              | Description                                                  |
|---------------------|--------------------------------------------------------------|
| **Execution Time**  | Real time measured during browser automation (2-5s)          |
| **Screenshots**     | Real PNG screenshots captured after each step                |
| **Performance**     | Actual page load times per step                              |
| **Pass/Fail**       | Based on actual execution — checks expected outcome on page  |
| **Failure Diagnosis** | Generated from actual page state (errors, available elements) |
