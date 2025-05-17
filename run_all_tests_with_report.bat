@echo off
echo ===================================================
echo Running Complete Test Framework with Allure Reports
echo ===================================================

REM Clean previous results
echo Cleaning previous test results...
IF EXIST allure-results rmdir /s /q allure-results
IF EXIST allure-report rmdir /s /q allure-report
mkdir allure-results

REM Set timestamp for report
set timestamp=%date:~-4,4%-%date:~-7,2%-%date:~-10,2%_%time:~0,2%-%time:~3,2%-%time:~6,2%
set timestamp=%timestamp: =0%

echo.
echo ===================================================
echo Running all tests...
echo ===================================================
echo.

REM Run all tests with Allure reporting
python -m pytest -v TEST_CLASS/ --alluredir=allure-results

echo.
echo ===================================================
echo Tests execution completed
echo ===================================================
echo.

REM Generate Allure report
echo Generating Allure report...
allure generate allure-results -o allure-report --clean

echo.
echo ===================================================
echo Opening Allure report...
echo ===================================================
echo.

REM Open the report
start allure-report\index.html

echo.
echo ===================================================
echo Report is available at: %CD%\allure-report\index.html
echo ===================================================
echo.

pause
