@echo off
echo ===================================================
echo Running POM Classes and Test Classes (Subset)
echo ===================================================
echo.

REM Clean previous results
echo Cleaning previous test results...
IF EXIST allure-results rmdir /s /q allure-results
mkdir allure-results

echo.
echo ===================================================
echo Running Login and Dashboard Tests...
echo ===================================================
echo.

REM Run only the Login and Dashboard test classes
python -m pytest -v .\TEST_CLASS\Test_Login.py .\TEST_CLASS\Test_Dashboard.py --alluredir=allure-results

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
echo Opening Allure report in Microsoft Edge...
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
