@echo off
REM Clean previous results
IF EXIST allure-results rmdir /s /q allure-results

REM Run database tests with Allure reporting
python -m pytest -v .\TEST_CLASS\Test_Database.py .\TEST_CLASS\Test_Login_DB_Validation.py --alluredir=allure-results

echo.
echo Tests execution completed. Run 'view_report.bat' to see the Allure report.
