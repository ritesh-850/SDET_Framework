 @echo off
echo ===================================================
echo Fixing Allure Report Generation
echo ===================================================
echo.

REM Clean previous results
echo Cleaning previous test results...
IF EXIST allure-results rmdir /s /q allure-results
IF EXIST allure-report rmdir /s /q allure-report
mkdir allure-results

echo.
echo ===================================================
echo Running Tests with Full Path...
echo ===================================================
echo.

REM Run tests with full path
python -m pytest -v .\TEST_CLASS\Test_Login.py --alluredir=allure-results

echo.
echo ===================================================
echo Generating Allure Report...
echo ===================================================
echo.

REM Generate Allure report
allure generate allure-results -o allure-report --clean

echo.
echo ===================================================
echo Opening Allure Report in Microsoft Edge...
echo ===================================================
echo.

REM Open the report in Microsoft Edge
start msedge "%CD%\allure-report\index.html"

echo.
echo ===================================================
echo Report is available at: %CD%\allure-report\index.html
echo ===================================================
echo.

pause
