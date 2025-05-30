@echo off
echo ===================================================
echo Running Database Tests
echo ===================================================
echo.

REM Clean previous results
echo Cleaning previous test results...
IF EXIST allure-results rmdir /s /q allure-results
mkdir allure-results

echo.
echo ===================================================
echo Running Database Tests...
echo ===================================================
echo.

REM Run database tests with Allure reporting
python -m pytest -v .\DB_TESTS\ --alluredir=allure-results

echo.
echo ===================================================
echo Tests execution completed
echo ===================================================
echo.

echo Run 'view_report.bat' to see the Allure report.

pause