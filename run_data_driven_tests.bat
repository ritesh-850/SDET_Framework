@echo off
echo ===================================================
echo Running Data-Driven Tests
echo ===================================================
echo.

REM Clean previous results
echo Cleaning previous test results...
IF EXIST allure-results rmdir /s /q allure-results
mkdir allure-results

echo.
echo ===================================================
echo Running Data-Driven Tests...
echo ===================================================
echo.

REM Run data-driven tests with Allure reporting
python -m pytest -v .\DATA_DRIVEN_TESTS\ --alluredir=allure-results

echo.
echo ===================================================
echo Tests execution completed
echo ===================================================
echo.

echo Run 'view_report.bat' to see the Allure report.

pause
