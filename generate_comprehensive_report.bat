@echo off
echo ===================================================
echo Generating Comprehensive Allure Report
echo ===================================================
echo.

REM Clean previous results
echo Cleaning previous test results...
IF EXIST allure-results rmdir /s /q allure-results
IF EXIST allure-report rmdir /s /q allure-report
mkdir allure-results

echo.
echo ===================================================
echo Running Login Tests...
echo ===================================================
echo.

REM Run Login tests
python -m pytest -v TEST_CLASS/Test_Login.py TEST_CLASS/Test_Login_DataDriven.py::TestLoginDataDriven::test_login_with_different_credentials[ritesh@123-Ritesh@123-Dashboard-pass] --alluredir=allure-results

echo.
echo ===================================================
echo Running Dashboard Tests...
echo ===================================================
echo.

REM Run Dashboard tests
python -m pytest -v TEST_CLASS/Test_Dashboard.py --alluredir=allure-results

echo.
echo ===================================================
echo Running Profile Tests...
echo ===================================================
echo.

REM Run Profile tests
python -m pytest -v TEST_CLASS/Test_Profile.py --alluredir=allure-results

echo.
echo ===================================================
echo Running Logout Tests...
echo ===================================================
echo.

REM Run Logout tests
python -m pytest -v TEST_CLASS/Test_Logout.py --alluredir=allure-results

echo.
echo ===================================================
echo Running Course Content Tests...
echo ===================================================
echo.

REM Run Course Content tests
python -m pytest -v TEST_CLASS/Test_CourseContent.py --alluredir=allure-results

echo.
echo ===================================================
echo Running Assignment Tests...
echo ===================================================
echo.

REM Run Assignment tests
python -m pytest -v TEST_CLASS/Test_Assignment.py --alluredir=allure-results

echo.
echo ===================================================
echo Generating Allure Report...
echo ===================================================
echo.

REM Generate Allure report
allure generate allure-results -o allure-report --clean

echo.
echo ===================================================
echo Opening Allure Report...
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
