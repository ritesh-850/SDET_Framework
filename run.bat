@echo off
echo ===================================================
echo Running All Tests with Allure Reporting
echo ===================================================
echo.

REM Clean previous results
echo Cleaning previous test results...
IF EXIST allure-results rmdir /s /q allure-results
mkdir allure-results

echo.
echo ===================================================
echo Running all tests...
echo ===================================================
echo.

REM Run tests with Allure reporting
python -m pytest -v TEST_CLASS --alluredir=allure-results

echo.
echo ===================================================
echo Tests execution completed
echo ===================================================
echo.

echo Run 'view_report.bat' to see the Allure report.
echo Or run 'run_framework.bat' for more options.

pause