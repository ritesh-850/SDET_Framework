# Allure Report Guide for BTES LMS Test Framework

This guide explains how to generate, interpret, and use the Allure reports for the BTES LMS Test Framework.

## Generating the Allure Report

### Option 1: Using the Batch File

The simplest way to run all tests and generate the Allure report is to use the provided batch file:

```
.\run_all_tests_with_report.bat
```

This will:
1. Clean previous test results
2. Run all tests in the framework
3. Generate the Allure report
4. Open the report in your default web browser

### Option 2: Manual Steps

If you prefer to run tests selectively or have more control over the process, you can follow these steps:

1. **Clean previous results**:
   ```
   Remove-Item -Path allure-results -Recurse -Force -ErrorAction SilentlyContinue
   mkdir allure-results
   ```

2. **Run tests with Allure reporting**:
   ```
   python -m pytest -v TEST_CLASS/ --alluredir=allure-results
   ```
   
   To run specific tests:
   ```
   python -m pytest -v TEST_CLASS/Test_Login.py TEST_CLASS/Test_Dashboard.py --alluredir=allure-results
   ```

3. **Generate the Allure report**:
   ```
   allure generate allure-results -o allure-report --clean
   ```

4. **Open the report in a web browser**:
   ```
   start allure-report\index.html
   ```

### Option 3: Interactive Framework Runner

For more options, you can use the interactive framework runner:

```
.\run_framework.bat
```

This provides a menu with multiple options for running tests and generating reports.

## Understanding the Allure Report

The Allure report provides a comprehensive view of your test execution results. Here's what you can find in the report:

### 1. Dashboard

The dashboard provides an overview of the test execution:

- **ALLURE REPORT**: Shows the total number of tests and their status (passed, failed, skipped, broken)
- **TREND**: Shows the trend of test results over time (if you have multiple test runs)
- **CATEGORIES**: Shows the distribution of test failures by category
- **SUITES**: Shows the test suites and their status
- **ENVIRONMENT**: Shows the environment information (if configured)
- **EXECUTORS**: Shows information about the test executor
- **HISTORY TREND**: Shows the trend of test results over time

### 2. Suites

The Suites tab shows a hierarchical view of your test suites and test cases:

- Each test class is shown as a suite
- Each test method is shown as a test case
- You can see the status, duration, and severity of each test
- You can click on a test to see detailed information

### 3. Graphs

The Graphs tab provides various visualizations of your test results:

- **Status**: Shows the distribution of test statuses
- **Severity**: Shows the distribution of test severities
- **Duration**: Shows the distribution of test durations
- **Retries**: Shows the number of retries for each test (if configured)

### 4. Timeline

The Timeline tab shows the chronological execution of your tests:

- Each test is shown as a bar on the timeline
- The length of the bar represents the duration of the test
- The color of the bar represents the status of the test
- You can see parallel test execution if applicable

### 5. Behaviors

The Behaviors tab organizes tests by features and stories:

- Tests are grouped by the `@allure.feature` annotation
- Within each feature, tests are grouped by the `@allure.story` annotation
- This provides a business-oriented view of your test results

### 6. Categories

The Categories tab groups test failures by category:

- Each category represents a type of failure
- You can see the number of tests in each category
- You can click on a category to see the tests in that category

### 7. Test Cases

The Test Cases tab shows a list of all test cases:

- You can see the status, duration, and severity of each test
- You can click on a test to see detailed information
- You can filter tests by status, severity, or other criteria

## Detailed Test View

When you click on a test case, you can see detailed information about the test:

1. **Overview**: Shows the test name, status, duration, and severity
2. **Steps**: Shows the steps executed during the test (based on `allure.step` annotations)
3. **Attachments**: Shows screenshots, logs, and other attachments captured during the test
4. **Parameters**: Shows the parameters used for the test (for parameterized tests)
5. **History**: Shows the history of the test over time (if available)

## Interpreting Test Results

### Test Status

- **Passed**: The test completed successfully
- **Failed**: The test failed due to an assertion error
- **Broken**: The test failed due to an exception
- **Skipped**: The test was skipped (e.g., due to a dependency on a failed test)

### Test Severity

Tests are categorized by severity:

- **Blocker**: Critical functionality that must work
- **Critical**: Important functionality that should work
- **Normal**: Regular functionality
- **Minor**: Minor functionality
- **Trivial**: Trivial functionality

### Attachments

The framework captures various attachments during test execution:

- **Screenshots**: Captured at key points during the test
- **Page Source**: HTML source of the page at the time of failure
- **Logs**: Test execution logs
- **Error Messages**: Detailed error messages for failed tests

## Best Practices

1. **Use Descriptive Test Names**: Make sure your test names clearly describe what they're testing
2. **Add Steps**: Use `allure.step` to break down your tests into logical steps
3. **Capture Screenshots**: Capture screenshots at key points in your tests
4. **Add Severity**: Use `allure.severity` to indicate the importance of each test
5. **Group Tests**: Use `allure.feature` and `allure.story` to group related tests
6. **Add Descriptions**: Use `allure.description` to provide detailed test descriptions

## Troubleshooting

### Common Issues

1. **Missing Allure Report**: Make sure you have Allure installed and in your PATH
2. **Empty Report**: Make sure you're running tests with the `--alluredir` option
3. **Missing Screenshots**: Make sure you're capturing screenshots using `allure.attach`
4. **Incorrect Test Status**: Make sure you're using assertions correctly

### Solutions

1. **Install Allure**:
   ```
   scoop install allure
   ```

2. **Check Allure Installation**:
   ```
   allure --version
   ```

3. **Clean Allure Results**:
   ```
   Remove-Item -Path allure-results -Recurse -Force -ErrorAction SilentlyContinue
   ```

4. **Run Tests with Allure Reporting**:
   ```
   python -m pytest -v TEST_CLASS/ --alluredir=allure-results
   ```

## Sharing the Report

To share the Allure report with others:

1. **Zip the Report**:
   ```
   Compress-Archive -Path allure-report -DestinationPath allure-report.zip
   ```

2. **Share the ZIP File**: Recipients can extract the ZIP file and open `index.html` in their browser

3. **Host the Report**: You can host the report on a web server or GitHub Pages

4. **Use Allure Server**:
   ```
   allure serve allure-results
   ```
   This starts a local web server that serves the report.

## Conclusion

The Allure report provides a comprehensive view of your test execution results, making it easy to identify issues and track the quality of your application over time. By following the guidelines in this document, you can effectively generate, interpret, and use Allure reports for the BTES LMS Test Framework.
