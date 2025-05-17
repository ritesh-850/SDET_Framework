# BTES LMS Test Automation Framework

This is a Selenium-based test automation framework that follows the Page Object Model (POM) design pattern. It's structured to test a learning management system (LMS) at https://online.btes.co.in/login/index.php.

## Framework Structure

- `POM_CLASS/`: Contains page object classes
- `TEST_CLASS/`: Contains test classes
- `conftest.py`: Contains pytest fixtures and hooks
- `run.bat`: Script to run tests with Allure reporting
- `view_report.bat`: Script to view Allure reports

## Prerequisites

1. Python 3.x installed
2. Chrome browser installed
3. Allure command-line tool installed

## Installation

1. Clone this repository
2. Run `install_packages.bat` to install required Python packages
3. Install Allure command-line tool:

### Installing Allure Command-line Tool

#### For Windows:
1. Install Scoop (if not already installed):
   ```
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   irm get.scoop.sh | iex
   ```
2. Install Allure using Scoop:
   ```
   scoop install allure
   ```

#### For Mac:
```
brew install allure
```

#### For Linux:
```
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure
```

## Running Tests

1. Run tests with Allure reporting:
   ```
   run.bat
   ```

2. View Allure report:
   ```
   view_report.bat
   ```

## Allure Report Features

The Allure report provides:
- Test execution summary
- Detailed test steps
- Screenshots at key points
- Automatic screenshots on test failures
- Test categorization by severity, feature, and story
- Test execution timeline

## Framework Components

1. **Page Objects (`POM_CLASS/`):**
   - `Login_Page_Object.py`: Handles login functionality
   - `Dashboard_Page_Object.py`: Dashboard page interactions
   - `SDET_Page_Object.py`: SDET course page interactions
   - `Calender_Page_Object.py`: Calendar page interactions
   - `Profile_Page_Object.py`: User profile page interactions
   - `Logout_page_object.py`: Logout functionality

2. **Test Classes (`TEST_CLASS/`):**
   - `Test_Login.py`: Tests login functionality
   - `Test_Dashboard.py`: Tests dashboard functionality
   - `Test_SDET.py`: Tests SDET course page
   - `Test_Calender.py`: Tests calendar functionality
   - `Test_Profile.py`: Tests profile page
   - `Test_Logout.py`: Tests logout functionality
