# Allure Report Summary for BTES LMS Test Framework

## Overview

The Allure report has been generated for the BTES LMS Test Framework and includes the results of the following test suites:

1. **Login Tests** - Basic login functionality
2. **Dashboard Tests** - Dashboard navigation and functionality
3. **Profile Tests** - User profile functionality
4. **Logout Tests** - Logout functionality
5. **Data-Driven Login Tests** - Login with different credentials

## Test Statistics

- **Total Tests**: 5
- **Passed Tests**: 5
- **Failed Tests**: 0
- **Skipped Tests**: 0
- **Test Duration**: Approximately 80 seconds

## Test Suites

### 1. Login Tests (Test_Login.py)
- **test_login**: Verifies that a user can successfully log in with valid credentials
- **Status**: Passed
- **Duration**: Approximately 20 seconds
- **Screenshots**: Login page, After login page

### 2. Dashboard Tests (Test_Dashboard.py)
- **test_dashboard**: Verifies that the dashboard page loads correctly after login
- **Status**: Passed
- **Duration**: Approximately 18 seconds
- **Screenshots**: Dashboard page

### 3. Profile Tests (Test_Profile.py)
- **test_profile**: Verifies that the user profile page loads correctly
- **Status**: Passed
- **Duration**: Approximately 10 seconds
- **Screenshots**: Profile page

### 4. Logout Tests (Test_Logout.py)
- **test_logout**: Verifies that a user can successfully log out
- **Status**: Passed
- **Duration**: Approximately 8 seconds
- **Screenshots**: Before logout, After logout

### 5. Data-Driven Login Tests (Test_Login_DataDriven.py)
- **test_login_with_different_credentials[ritesh@123-Ritesh@123-Dashboard-pass]**: Verifies login with valid credentials
- **Status**: Passed
- **Duration**: Approximately 23 seconds
- **Screenshots**: Login page, After login page

## Test Steps

Each test includes detailed steps with screenshots:

1. **Navigate to the application URL**
2. **Enter login credentials** (for login tests)
3. **Click login button** (for login tests)
4. **Verify successful login** (for login tests)
5. **Navigate to specific pages** (for dashboard, profile tests)
6. **Perform actions** (for logout tests)
7. **Verify expected results**

## Attachments

The report includes various attachments:

- **Screenshots**: Captured at key points during test execution
- **Page Source**: HTML source of the page at the time of failure (if any)
- **Error Messages**: Detailed error messages for failed tests (if any)

## Report Features

The Allure report provides several features for analyzing test results:

1. **Dashboard**: Overview of test execution results
2. **Suites**: Hierarchical view of test suites and test cases
3. **Graphs**: Various graphs showing test execution statistics
4. **Timeline**: Timeline view of test execution
5. **Behaviors**: Tests organized by features and stories
6. **Categories**: Tests categorized by failure types

## How to View the Report

The report is available at:
```
[Your Project Directory]\allure-report\index.html
```

It has been opened in Microsoft Edge for viewing.

## Next Steps

1. **Run More Tests**: Add more tests to the report by running additional test classes
2. **Analyze Results**: Review the report to identify any issues or areas for improvement
3. **Share Report**: Share the report with stakeholders by zipping the allure-report folder
4. **Integrate with CI/CD**: Configure your CI/CD pipeline to generate Allure reports automatically

## Conclusion

The Allure report provides a comprehensive view of the test execution results for the BTES LMS Test Framework. All tests have passed, indicating that the basic functionality of the application is working as expected.
